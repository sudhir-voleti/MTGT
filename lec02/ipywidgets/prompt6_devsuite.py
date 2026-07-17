# prompt6_devsuite.py
# ═══════════════════════════════════════════════════════════════════════
# Panel Traction: Dynamic Account Scoring — ipywidgets (V3)
# Updated for FinScale V2 data with corrected V-A-E mapping
# ═══════════════════════════════════════════════════════════════════════

# ── Quiet install ─────────────────────────────────────────────────────
import subprocess, sys
for pkg in ["ipywidgets", "scikit-learn", "pandas", "matplotlib", "seaborn", "IPython"]:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg])

# ── Imports ─────────────────────────────────────────────────────────────
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output, FileLink
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from datetime import datetime
import io
import warnings
warnings.filterwarnings('ignore')

# ── Global State ──────────────────────────────────────────────────────────
state = {
    'df_raw': None,
    'df_processed': None,
    'account_col': None,
    'period_col': None,
    'numeric_cols': [],
    'scored_long': None,
    'scored_wide': None,
    'k': 3,
    'centroids': None,
    'cluster_sizes': None,
    'reflection': ""
}

# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: UPLOAD & CONFIGURE
# ═══════════════════════════════════════════════════════════════════════

upload_widget = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='📁 Upload CSV',
    layout=widgets.Layout(width='200px')
)

upload_status = widgets.HTML(value="<p style='color:#888;'>Upload a panel CSV to begin.</p>")
preview_area = widgets.Output()

account_dropdown = widgets.Dropdown(
    options=['(Upload first)'],
    value='(Upload first)',
    description='Account ID:',
    disabled=True,
    layout=widgets.Layout(width='300px')
)

period_dropdown = widgets.Dropdown(
    options=['(Upload first)'],
    value='(Upload first)',
    description='Period:',
    disabled=True,
    layout=widgets.Layout(width='300px')
)

configure_btn = widgets.Button(
    description='✅ Configure Panel',
    button_style='primary',
    disabled=True,
    layout=widgets.Layout(width='180px')
)

config_status = widgets.HTML(value="<p>Upload and select fields first.</p>")
stats_area = widgets.Output()

# ── Upload Handler ────────────────────────────────────────────────────

def on_upload(change):
    if not upload_widget.value:
        return

    uploaded = list(upload_widget.value.values())[0]
    content = uploaded['content']

    try:
        df = pd.read_csv(io.BytesIO(content))
        state['df_raw'] = df
        cols = df.columns.tolist()

        likely_account = [c for c in cols if any(x in c.lower() for x in ['account', 'id', 'tenant', 'customer', 'user'])]
        likely_period = [c for c in cols if any(x in c.lower() for x in ['period', 'month', 'time', 'week', 'quarter'])]

        account_dropdown.options = cols
        account_dropdown.value = likely_account[0] if likely_account else cols[0]
        account_dropdown.disabled = False

        period_dropdown.options = cols
        period_dropdown.value = likely_period[0] if likely_period else cols[0]
        period_dropdown.disabled = False

        configure_btn.disabled = False

        upload_status.value = f"<p style='color:green;'>✅ Loaded: <b>{len(df):,}</b> rows × {len(df.columns)} columns</p>"

        with preview_area:
            clear_output()
            display(HTML(f"<h4>Data Preview (first 10 rows)</h4>"))
            display(df.head(10).style.set_properties(**{'font-size': '11px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f5f5f5'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        n_accounts = df[likely_account[0]].nunique() if likely_account else 'N/A'
        n_periods = len(df[likely_period[0]].unique()) if likely_period else 'N/A'
        numeric_count = len(df.select_dtypes(include=[np.number]).columns)

        with stats_area:
            clear_output()
            display(HTML(f"""
            <div style="background:#f8f9fa; padding:12px; border-radius:6px; border:1px solid #dee2e6;">
                <b>Dataset Overview</b><br>
                • Rows: {len(df):,} | Columns: {len(df.columns)}<br>
                • Unique accounts: {n_accounts} | Periods: {n_periods}<br>
                • Numeric columns: {numeric_count}<br><br>
                <b>All columns:</b><br>
                {', '.join(cols)}
            </div>
            """))

    except Exception as e:
        upload_status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"

upload_widget.observe(on_upload, names='value')

# ── Configure Handler ─────────────────────────────────────────────────

def on_configure(b):
    df = state['df_raw']
    ac = account_dropdown.value
    pc = period_dropdown.value

    if ac == pc:
        config_status.value = "<p style='color:red;'>❌ Account and Period must be different.</p>"
        return

    state['df_processed'] = df
    state['account_col'] = ac
    state['period_col'] = pc
    state['numeric_cols'] = [c for c in df.columns if c not in [ac, pc] and pd.api.types.is_numeric_dtype(df[c])]

    if len(state['numeric_cols']) < 2:
        config_status.value = "<p style='color:red;'>❌ Need at least 2 numeric variables.</p>"
        return

    config_status.value = f"<p style='color:green;'>✅ Panel configured: <b>{df[ac].nunique():,}</b> accounts × <b>{df[pc].nunique()}</b> periods. <b>{len(state['numeric_cols'])}</b> numeric variables.</p>"

    update_mapping_tab()
    tabs.selected_index = 1

configure_btn.on_click(on_configure)

upload_section = widgets.VBox([
    widgets.HTML("<h2>📁 Section 1: Upload & Configure</h2>"),
    widgets.HBox([upload_widget, upload_status]),
    preview_area,
    widgets.HBox([account_dropdown, period_dropdown, configure_btn]),
    config_status,
    stats_area
])

# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: MAP TRACTION COMPONENTS
# ═══════════════════════════════════════════════════════════════════════

mapping_status = widgets.HTML(value="<p>Configure panel in Section 1 first.</p>")

# Variable architecture guidance - updated for FinScale V2
var_guidance = widgets.HTML(value="""
<div style="background:#fff3cd; padding:10px; border-radius:6px; border-left:4px solid #ffc107; margin-bottom:10px;">
<b>💡 V-A-E Variable Architecture (FinScale V2)</b><br><br>
<b>Value</b> (Product features customer experiences):<br>
• <code>credit_limit_inr</code> — structural credit line<br>
• <code>plan_tier</code> — Basic/Pro/Enterprise benefits<br>
• <code>card_plastic_variant</code> — Classic/Premium/Elite prestige<br>
• <code>departmental_card_span</code> — embedding depth (# departments using cards)<br><br>
<b>Access</b> (Acquisition efficiency & friction):<br>
• <code>acquisition_channel</code> — Performance Ads / Founder Referral / Outbound Sales<br>
• <code>marketing_promo_coupon_code</code> — WELCOME50 / STARTUP100 / REFER50 / NONE<br>
• <code>onboarding_device_type</code> — Mobile / Desktop / Tablet<br><br>
<b>Evidence</b> (Behavioral proof of value realization):<br>
• <code>monthly_transaction_count</code> — usage velocity<br>
• <code>monthly_spend_volume_inr</code> — spend depth<br>
• <code>credit_utilization_ratio</code> — credit engagement<br>
• <code>average_settlement_delay_days</code> — payment discipline (lower = better)<br>
• <code>late_payment_flag</code> — 0/1 delinquency signal<br>
• <code>active_flag</code> — 0/1 retention signal<br>
• <code>monthly_active_days</code> — engagement breadth<br><br>
<b>Noise</b> (NOT in any traction bucket):<br>
• <code>company_size_employees</code> — firm characteristic (not product feature)<br>
• <code>tenure_months_at_onboarding</code> — structural firm age<br>
• <code>industry_vertical</code> — sector classification<br>
• <code>customer_support_tickets</code> — post-hoc operational noise<br>
• <code>app_session_duration_minutes</code> — engagement noise<br>
• <code>referral_attempts_count</code> — viral noise<br><br>
<i><b>⚠️ Tip:</b> Only map variables to ONE component. If a variable fits multiple, pick the best fit and note it in your reflection.</i>
</div>
""")

value_check = widgets.SelectMultiple(
    options=[],
    description='Value:',
    rows=6,
    layout=widgets.Layout(width='250px')
)
access_check = widgets.SelectMultiple(
    options=[],
    description='Access:',
    rows=6,
    layout=widgets.Layout(width='250px')
)
evidence_check = widgets.SelectMultiple(
    options=[],
    description='Evidence:',
    rows=6,
    layout=widgets.Layout(width='250px')
)

reflection_box = widgets.Textarea(
    value='',
    placeholder='Reflect on your mapping...',
    description='Reflection:',
    layout=widgets.Layout(width='500px', height='80px')
)

weight_editor = widgets.Textarea(
    value='',
    placeholder='variable=Component:weight (one per line)',
    description='Weights:',
    layout=widgets.Layout(width='500px', height='120px')
)

clear_weights_btn = widgets.Button(description='🔄 Clear All', button_style='warning', layout=widgets.Layout(width='100px'))
compute_btn = widgets.Button(description='📊 Compute & Cluster', button_style='success', layout=widgets.Layout(width='180px'))
compute_btn.disabled = True

def update_mapping_tab():
    cols = state['numeric_cols']
    value_check.options = cols
    access_check.options = cols
    evidence_check.options = cols
    mapping_status.value = f"<p style='color:green;'>✅ <b>{len(cols)}</b> numeric variables available. Select variables for each component.</p>"
    compute_btn.disabled = False

def build_weights_text(*args):
    lines = []
    for v in value_check.value:
        lines.append(f"{v}=Value:1.0")
    for v in access_check.value:
        lines.append(f"{v}=Access:1.0")
    for v in evidence_check.value:
        lines.append(f"{v}=Evidence:1.0")
    weight_editor.value = "\n".join(lines)

def on_clear_weights(b):
    value_check.value = ()
    access_check.value = ()
    evidence_check.value = ()
    weight_editor.value = ''

value_check.observe(build_weights_text, names='value')
access_check.observe(build_weights_text, names='value')
evidence_check.observe(build_weights_text, names='value')
clear_weights_btn.on_click(on_clear_weights)

mapping_section = widgets.VBox([
    widgets.HTML("<h2>🔧 Section 2: Map Traction Components</h2>"),
    var_guidance,
    widgets.HTML("<p><b>Step 1:</b> Select variables for Value (product features), Access (acquisition), Evidence (behavioral).</p>"),
    widgets.HBox([value_check, access_check, evidence_check]),
    widgets.HTML("<p><b>Step 2:</b> Reflect on your mapping. Which variables were ambiguous? Did you force any into a bucket?</p>"),
    reflection_box,
    widgets.HTML("<p><b>Step 3:</b> Review auto-generated weights (edit if needed). Format: <code>variable=Component:weight</code></p>"),
    widgets.HBox([weight_editor, widgets.VBox([clear_weights_btn, compute_btn])]),
    mapping_status
])

# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: TRACTION OVER TIME
# ═══════════════════════════════════════════════════════════════════════

k_slider = widgets.IntSlider(value=3, min=2, max=6, step=1, description='Clusters K:', layout=widgets.Layout(width='300px'))
view_dropdown = widgets.Dropdown(
    options=['Cluster Means', 'Full Sample'],
    value='Cluster Means',
    description='View:',
    layout=widgets.Layout(width='200px')
)
account_dropdown_view = widgets.Dropdown(
    options=['(None)'],
    value='(None)',
    description='Account:',
    layout=widgets.Layout(width='200px')
)

results_status = widgets.HTML(value="<p>Map variables in Section 2, then click Compute.</p>")
scree_output = widgets.Output()
centroids_output = widgets.Output()
trajectory_output = widgets.Output()
summary_output = widgets.Output()

# Download outputs
download_area = widgets.Output()

export_wide_btn = widgets.Button(description='📊 Wide CSV', button_style='info', layout=widgets.Layout(width='120px'))
export_long_btn = widgets.Button(description='📊 Long CSV', button_style='info', layout=widgets.Layout(width='120px'))
export_report_btn = widgets.Button(description='📄 Report TXT', button_style='info', layout=widgets.Layout(width='120px'))
export_status = widgets.HTML(value="")

# ── Parse Weights ─────────────────────────────────────────────────────

def parse_weights(weight_text):
    weights = {}
    if not weight_text:
        return weights
    for line in weight_text.strip().split("\n"):
        if "=" in line:
            parts = line.split("=")
            if len(parts) == 2:
                var = parts[0].strip()
                comp_weight = parts[1].strip().split(":")
                if len(comp_weight) == 2:
                    comp = comp_weight[0].strip()
                    try:
                        w = float(comp_weight[1].strip())
                    except:
                        w = 0
                    if var not in weights:
                        weights[var] = {"Value": 0, "Access": 0, "Evidence": 0}
                    weights[var][comp] = w
    return weights

# ── Compute Handler ───────────────────────────────────────────────────

def on_compute(b):
    df = state['df_processed']
    ac = state['account_col']
    pc = state['period_col']
    weight_text = weight_editor.value
    k = k_slider.value
    state['reflection'] = reflection_box.value

    if df is None:
        results_status.value = "<p style='color:red;'>❌ Configure panel first.</p>"
        return

    weights = parse_weights(weight_text)
    if not weights:
        results_status.value = "<p style='color:red;'>❌ Set weights first.</p>"
        return

    value_vars = [v for v, w in weights.items() if w.get("Value", 0) > 0]
    access_vars = [v for v, w in weights.items() if w.get("Access", 0) > 0]
    evidence_vars = [v for v, w in weights.items() if w.get("Evidence", 0) > 0]

    if not value_vars or not access_vars or not evidence_vars:
        results_status.value = "<p style='color:red;'>❌ Each component needs at least one variable.</p>"
        return

    # Normalize
    numeric_cols = state['numeric_cols']
    df_norm = df.copy()
    for col in numeric_cols:
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max > col_min:
            df_norm[col] = (df[col] - col_min) / (col_max - col_min)
        else:
            df_norm[col] = 0.5

    # Score
    def score_row(row):
        v_num = sum(row[v] * weights[v]["Value"] for v in value_vars)
        v_den = sum(weights[v]["Value"] for v in value_vars)
        v_score = v_num / v_den if v_den > 0 else 0

        a_num = sum(row[v] * weights[v]["Access"] for v in access_vars)
        a_den = sum(weights[v]["Access"] for v in access_vars)
        a_score = a_num / a_den if a_den > 0 else 0

        e_num = sum(row[v] * weights[v]["Evidence"] for v in evidence_vars)
        e_den = sum(weights[v]["Evidence"] for v in evidence_vars)
        e_score = e_num / e_den if e_den > 0 else 0

        return pd.Series({
            "Value_score": round(v_score, 4),
            "Access_score": round(a_score, 4),
            "Evidence_score": round(e_score, 4),
            "Traction_quotient": round(v_score * a_score * e_score, 4)
        })

    scores = df_norm[numeric_cols].apply(score_row, axis=1)

    scored_long = df.copy()
    scored_long["Value_score"] = scores["Value_score"].values
    scored_long["Access_score"] = scores["Access_score"].values
    scored_long["Evidence_score"] = scores["Evidence_score"].values
    scored_long["Traction_quotient"] = scores["Traction_quotient"].values
    state['scored_long'] = scored_long

    # Wide format
    wide = scored_long.pivot(index=ac, columns=pc, values="Traction_quotient")
    wide.columns = [f"Period_{c}" for c in wide.columns]
    wide = wide.reset_index()
    period_cols = [c for c in wide.columns if c.startswith("Period_")]
    wide[period_cols] = wide[period_cols].fillna(wide[period_cols].mean())

    # Cluster
    X = wide.drop(columns=[ac]).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Scree
    wcss = []
    ks = range(1, min(7, len(X)))
    for ki in ks:
        km = KMeans(n_clusters=ki, random_state=42, n_init=10)
        km.fit(X_scaled)
        wcss.append(km.inertia_)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(list(ks), wcss, 'bo-', linewidth=2, markersize=8)
    ax.set_xlabel('K', fontsize=11)
    ax.set_ylabel('WCSS', fontsize=11)
    ax.set_title('Scree Plot: Trajectory Clusters', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(list(ks))
    plt.tight_layout()

    with scree_output:
        clear_output()
        display(fig)
    plt.close(fig)

    # Final K-Means
    km_final = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km_final.fit_predict(X_scaled)
    wide["Cluster"] = labels
    state['scored_wide'] = wide
    state['k'] = k

    # Cluster sizes
    cluster_sizes = wide["Cluster"].value_counts().sort_index()
    state['cluster_sizes'] = cluster_sizes

    # Centroids with sizes
    centroids_data = []
    for i in range(k):
        cluster_data = wide[wide["Cluster"] == i]
        mean_traj = cluster_data[period_cols].mean()
        row = {"Cluster": f"Cluster {i+1}", "Size (n)": len(cluster_data)}
        for col in period_cols:
            row[col] = round(mean_traj[col], 4)
        centroids_data.append(row)
    centroids = pd.DataFrame(centroids_data)
    state['centroids'] = centroids

    with centroids_output:
        clear_output()
        display(HTML("<h4>Cluster Centroids (with Segment Sizes)</h4>"))
        display(centroids.style.set_properties(**{'font-size': '11px'}).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#e8f4f8'), ('font-weight', 'bold')]},
            {'selector': 'td', 'props': [('border', '1px solid #eee')]}
        ]))

    # Summary
    summary = wide.copy()
    summary["Mean_Traction"] = summary[period_cols].mean(axis=1).round(4)
    summary["Std_Traction"] = summary[period_cols].std(axis=1).round(4)
    summary["Trend"] = (summary[period_cols[-1]] - summary[period_cols[0]]).round(4)
    summary["Cluster_Label"] = [f"Cluster {l+1}" for l in labels]

    summary_display = summary[[ac, "Cluster_Label", "Mean_Traction", "Std_Traction", "Trend"] + period_cols[:3] + period_cols[-3:]]

    with summary_output:
        clear_output()
        display(HTML(f"<h4>Account Summary (showing {min(20, len(summary_display))} of {len(summary_display)} accounts)</h4>"))
        display(summary_display.head(20).style.set_properties(**{'font-size': '10px'}).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#f0f0f0'), ('font-weight', 'bold')]},
            {'selector': 'td', 'props': [('border', '1px solid #eee')]}
        ]))

    # Update account dropdown
    account_dropdown_view.options = ['(None)'] + sorted(df[ac].unique().tolist())[:100]
    account_dropdown_view.value = '(None)'

    # Generate initial trajectory plot
    generate_trajectory_plot()

    results_status.value = f"<p style='color:green;'>✅ Computed traction for <b>{len(df):,}</b> rows. Clustered <b>{len(wide):,}</b> accounts into <b>{k}</b> trajectory clusters.</p>"

    tabs.selected_index = 2

compute_btn.on_click(on_compute)

# ── Trajectory Plot ───────────────────────────────────────────────────

def generate_trajectory_plot():
    wide_df = state['scored_wide']
    k = state['k']
    view = view_dropdown.value
    account = account_dropdown_view.value

    if wide_df is None or wide_df.empty:
        return

    period_cols = [c for c in wide_df.columns if c.startswith("Period_")]
    if not period_cols:
        return

    periods = []
    for c in period_cols:
        try:
            periods.append(int(c.split("_")[1]))
        except:
            periods.append(c)

    sorted_pairs = sorted(zip(periods, period_cols), key=lambda x: x[0] if isinstance(x[0], (int, float)) else str(x[0]))
    periods = [p for p, _ in sorted_pairs]
    period_cols = [c for _, c in sorted_pairs]

    fig, ax = plt.subplots(figsize=(10, 5))

    if view == "Cluster Means":
        colors = plt.cm.Set2(np.linspace(0, 1, k))
        for i in range(k):
            cluster_data = wide_df[wide_df["Cluster"] == i]
            if len(cluster_data) == 0:
                continue
            mean_traj = cluster_data[period_cols].mean()
            size = state['cluster_sizes'].get(i, 0) if state['cluster_sizes'] is not None else len(cluster_data)
            ax.plot(periods, mean_traj, 'o-', linewidth=2.5, markersize=8, 
                   color=colors[i], label=f"Cluster {i+1} (n={size})")
        ax.set_title("Traction Trajectory by Cluster", fontsize=12, fontweight='bold')

    elif view == "Full Sample":
        mean_traj = wide_df[period_cols].mean()
        std_traj = wide_df[period_cols].std()
        ax.plot(periods, mean_traj, 'o-', linewidth=2.5, markersize=8, color='#2E86AB', label="Full Sample Mean")
        ax.fill_between(periods, mean_traj - std_traj, mean_traj + std_traj, alpha=0.2, color='#2E86AB', label="±1 SD")
        ax.set_title("Full Sample Traction Trajectory", fontsize=12, fontweight='bold')

    # Overlay account
    non_period = [c for c in wide_df.columns if not c.startswith("Period_") and c != "Cluster"]
    if non_period and account and account != '(None)' and account in wide_df[non_period[0]].values:
        acc_data = wide_df[wide_df[non_period[0]] == account]
        if len(acc_data) > 0:
            acc_traj = acc_data[period_cols].values[0]
            ax.plot(periods, acc_traj, 's--', linewidth=2, markersize=10, 
                   color='red', label=f"Account {account}", zorder=5)

    ax.set_xlabel("Period", fontsize=11)
    ax.set_ylabel("Traction Quotient", fontsize=11)
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    with trajectory_output:
        clear_output()
        display(fig)
    plt.close(fig)

def on_view_change(change):
    generate_trajectory_plot()

def on_account_change(change):
    generate_trajectory_plot()

view_dropdown.observe(on_view_change, names='value')
account_dropdown_view.observe(on_account_change, names='value')

# ── Export Handlers ───────────────────────────────────────────────────

def on_export_wide(b):
    wide = state['scored_wide']
    if wide is None:
        export_status.value = "<p style='color:red;'>❌ Compute first.</p>"
        return
    path = "/tmp/panel_traction_wide.csv"
    wide.to_csv(path, index=False)

    with download_area:
        clear_output()
        display(HTML(f"""
        <div style="background:#d4edda; padding:10px; border-radius:6px; border-left:4px solid #28a745;">
            <b>✅ Wide format saved</b><br>
            Path: {path}<br>
            Accounts: {len(wide):,}<br><br>
            <i>In Colab: run <code>from google.colab import files; files.download('{path}')</code></i><br>
            <i>In Jupyter: <a href="{FileLink(path).href}" target="_blank">Download wide CSV</a></i>
        </div>
        """))

    export_status.value = f"<p style='color:green;'>✅ Wide format saved to {path}</p>"

def on_export_long(b):
    long = state['scored_long']
    if long is None:
        export_status.value = "<p style='color:red;'>❌ Compute first.</p>"
        return
    path = "/tmp/panel_traction_long.csv"
    long.to_csv(path, index=False)

    with download_area:
        clear_output()
        display(HTML(f"""
        <div style="background:#d4edda; padding:10px; border-radius:6px; border-left:4px solid #28a745;">
            <b>✅ Long format saved</b><br>
            Path: {path}<br>
            Rows: {len(long):,}<br><br>
            <i>In Colab: run <code>from google.colab import files; files.download('{path}')</code></i><br>
            <i>In Jupyter: <a href="{FileLink(path).href}" target="_blank">Download long CSV</a></i>
        </div>
        """))

    export_status.value = f"<p style='color:green;'>✅ Long format saved to {path}</p>"

def on_export_report(b):
    wide = state['scored_wide']
    if wide is None:
        export_status.value = "<p style='color:red;'>❌ Compute first.</p>"
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    k = state['k']
    cluster_sizes = state['cluster_sizes']
    centroids = state['centroids']

    report = [
        "# Panel Traction Audit Report",
        "",
        f"Generated: {timestamp}",
        f"Accounts: {len(wide):,}",
        f"Clusters: {k}",
        "",
        "## Cluster Sizes",
        ""
    ]
    for i in range(k):
        size = cluster_sizes.get(i, 0) if cluster_sizes is not None else 0
        report.append(f"  Cluster {i+1}: {size} accounts ({size/len(wide)*100:.1f}%)")

    report.extend(["", "---", "", "## Cluster Centroids", ""])
    if centroids is not None:
        report.append(centroids.to_string(index=False))

    report.extend(["", "---", "", "## Reflection", "", state['reflection'] or "(No reflection)", "", "---", "", "*End of Report*"])

    path = "/tmp/panel_traction_report.txt"
    with open(path, "w") as f:
        f.write("\n".join(report))

    with download_area:
        clear_output()
        display(HTML(f"""
        <div style="background:#d4edda; padding:10px; border-radius:6px; border-left:4px solid #28a745;">
            <b>✅ Report saved</b><br>
            Path: {path}<br><br>
            <i>In Colab: run <code>from google.colab import files; files.download('{path}')</code></i><br>
            <i>In Jupyter: <a href="{FileLink(path).href}" target="_blank">Download report</a></i>
        </div>
        """))

    export_status.value = f"<p style='color:green;'>✅ Report saved to {path}</p>"

export_wide_btn.on_click(on_export_wide)
export_long_btn.on_click(on_export_long)
export_report_btn.on_click(on_export_report)

results_section = widgets.VBox([
    widgets.HTML("<h2>📈 Section 3: Traction Over Time</h2>"),
    widgets.HBox([k_slider, compute_btn]),
    results_status,
    widgets.HTML("<h4>Scree Plot</h4>"),
    scree_output,
    widgets.HTML("<h4>Cluster Centroids</h4>"),
    centroids_output,
    widgets.HTML("<h4>Trajectory Plot</h4>"),
    widgets.HBox([view_dropdown, account_dropdown_view]),
    trajectory_output,
    widgets.HTML("<h4>Account Summary</h4>"),
    summary_output,
    widgets.HTML("<h4>Export</h4>"),
    widgets.HBox([export_wide_btn, export_long_btn, export_report_btn]),
    export_status,
    download_area
])

# ═══════════════════════════════════════════════════════════════════════
# ASSEMBLE TABS
# ═══════════════════════════════════════════════════════════════════════

tabs = widgets.Tab(children=[upload_section, mapping_section, results_section])
tabs.set_title(0, '📁 Upload & Configure')
tabs.set_title(1, '🔧 Map Components')
tabs.set_title(2, '📈 Traction & Clusters')

display(tabs)
