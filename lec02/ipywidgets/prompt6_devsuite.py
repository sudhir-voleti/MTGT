# ═══════════════════════════════════════════════════════════════════════
# App 2: Panel Traction Over Time — Dynamic Account Scoring (ipywidgets)
# 3 tabs: Upload & Configure, Map Traction Components, Traction Over Time
# Paste into ONE Jupyter/Colab cell and run
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
from IPython.display import display, HTML, clear_output
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from datetime import datetime
import io
import warnings
warnings.filterwarnings('ignore')

# ── Global State ────────────────────────────────────────────────────────
state = {
    'df_raw': None,
    'df_processed': None,
    'account_col': None,
    'period_col': None,
    'numeric_cols': [],
    'dummy_cols': [],
    'scored_long': None,
    'scored_wide': None,
    'k': 3
}

# ═══════════════════════════════════════════════════════════════════════
# TAB 1: UPLOAD & CONFIGURE
# ═══════════════════════════════════════════════════════════════════════

file_in = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='📁 Upload CSV',
    layout=widgets.Layout(width='200px')
)

status = widgets.HTML(value="<p style='color:#888;'>Waiting for CSV upload...</p>")
preview_output = widgets.Output()
with preview_output:
    display(HTML("<p style='color:#888;'>Upload a panel CSV to see preview.</p>"))

desc_stats = widgets.Textarea(
    value="Upload CSV and configure fields.",
    description='Overview:',
    layout=widgets.Layout(width='100%', height='200px'),
    disabled=True
)

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
    layout=widgets.Layout(width='180px'),
    disabled=True
)

config_status = widgets.HTML(value="<p>Upload and select fields first.</p>")

tab1 = widgets.VBox([
    widgets.HTML("<h2>📁 Upload & Configure</h2>"),
    widgets.HBox([file_in, status]),
    widgets.HTML("<h4>Data Preview</h4>"),
    preview_output,
    widgets.HTML("<h4>Panel Configuration</h4>"),
    widgets.HBox([account_dropdown, period_dropdown, configure_btn]),
    config_status,
    widgets.HTML("<h4>Dataset Overview</h4>"),
    desc_stats
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 2: MAP TRACTION COMPONENTS
# ═══════════════════════════════════════════════════════════════════════

value_check = widgets.SelectMultiple(
    options=['(Configure panel first)'],
    value=(),
    description='Value:',
    rows=6,
    layout=widgets.Layout(width='250px'),
    disabled=True
)

access_check = widgets.SelectMultiple(
    options=['(Configure panel first)'],
    value=(),
    description='Access:',
    rows=6,
    layout=widgets.Layout(width='250px'),
    disabled=True
)

evidence_check = widgets.SelectMultiple(
    options=['(Configure panel first)'],
    value=(),
    description='Evidence:',
    rows=6,
    layout=widgets.Layout(width='250px'),
    disabled=True
)

reflection_box = widgets.Textarea(
    value='',
    placeholder='Reflect on your mapping...',
    description='Reflection:',
    layout=widgets.Layout(width='100%', height='80px')
)

weight_editor = widgets.Textarea(
    value='',
    placeholder='variable=Component:weight (one per line)',
    description='Weights:',
    layout=widgets.Layout(width='500px', height='120px')
)

clear_weights_btn = widgets.Button(
    description='🔄 Clear All',
    button_style='warning',
    layout=widgets.Layout(width='100px')
)

mapping_status = widgets.HTML(value="<p>Configure panel in Tab 1 first.</p>")

tab2 = widgets.VBox([
    widgets.HTML("<h2>🔧 Map Traction Components</h2>"),
    widgets.HTML("<p><b>Step 1:</b> Check variables for Value (utility), Access (reach), Evidence (behavioral).</p>"),
    widgets.HBox([value_check, access_check, evidence_check]),
    widgets.HTML("<p><b>Step 2:</b> Reflect on your mapping.</p>"),
    reflection_box,
    widgets.HTML("<p><b>Step 3:</b> Review auto-generated weights (edit if needed). Format: <code>variable=Component:weight</code></p>"),
    widgets.HBox([weight_editor, widgets.VBox([clear_weights_btn])]),
    mapping_status
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 3: TRACTION OVER TIME
# ═══════════════════════════════════════════════════════════════════════

k_slider = widgets.IntSlider(value=3, min=2, max=6, step=1, description='Clusters K:', layout=widgets.Layout(width='300px'))

run_btn = widgets.Button(
    description='📊 Compute & Cluster',
    button_style='success',
    layout=widgets.Layout(width='180px'),
    disabled=True
)

run_status = widgets.HTML(value="<p>Map variables in Tab 2, then click Compute.</p>")

scree_output = widgets.Output()
with scree_output:
    display(HTML("<p style='color:#888;'>Compute traction to see scree plot.</p>"))

centroids_output = widgets.Output()
with centroids_output:
    display(HTML("<p style='color:#888;'>Compute traction to see centroids.</p>"))

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
    disabled=True,
    layout=widgets.Layout(width='200px')
)

trajectory_output = widgets.Output()
with trajectory_output:
    display(HTML("<p style='color:#888;'>Compute traction to see trajectory plot.</p>"))

summary_output = widgets.Output()
with summary_output:
    display(HTML("<p style='color:#888;'>Compute traction to see summary.</p>"))

export_wide_btn = widgets.Button(description='📊 Wide CSV', button_style='info', layout=widgets.Layout(width='120px'), disabled=True)
export_long_btn = widgets.Button(description='📊 Long CSV', button_style='info', layout=widgets.Layout(width='120px'), disabled=True)
export_report_btn = widgets.Button(description='📄 Report TXT', button_style='info', layout=widgets.Layout(width='120px'), disabled=True)

export_status = widgets.HTML(value="<p>Compute traction, then export.</p>")

tab3 = widgets.VBox([
    widgets.HTML("<h2>📈 Traction Over Time</h2>"),
    widgets.HTML("<h3>Compute Traction, Cluster Trajectories, Visualize Dynamics</h3>"),
    widgets.HBox([k_slider, run_btn, run_status]),
    widgets.HTML("<h4>Scree Plot</h4>"),
    scree_output,
    widgets.HTML("<h4>Cluster Centroids</h4>"),
    centroids_output,
    widgets.HTML("<h4>Trajectory Plot</h4>"),
    widgets.HBox([view_dropdown, account_dropdown_view]),
    trajectory_output,
    widgets.HTML("<h4>Account-Level Summary</h4>"),
    summary_output,
    widgets.HTML("<h4>📥 Export</h4>"),
    widgets.HBox([export_wide_btn, export_long_btn, export_report_btn, export_status])
])

# ═══════════════════════════════════════════════════════════════════════
# ASSEMBLE TABS
# ═══════════════════════════════════════════════════════════════════════

tabs = widgets.Tab(children=[tab1, tab2, tab3])
tabs.set_title(0, '📁 Upload & Configure')
tabs.set_title(1, '🔧 Map Components')
tabs.set_title(2, '📈 Traction & Clusters')

# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

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

def build_weight_text(value_vars, access_vars, evidence_vars):
    lines = []
    all_vars = set((value_vars or []) + (access_vars or []) + (evidence_vars or []))
    for var in sorted(all_vars):
        if value_vars and var in value_vars:
            lines.append(f"{var}=Value:1.0")
        if access_vars and var in access_vars:
            lines.append(f"{var}=Access:1.0")
        if evidence_vars and var in evidence_vars:
            lines.append(f"{var}=Evidence:1.0")
    return "\n".join(lines)

def generate_trajectory_plot(wide_df, view, account, k):
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
            ax.plot(periods, mean_traj, 'o-', linewidth=2.5, markersize=8, 
                   color=colors[i], label=f"Cluster {i+1} (n={len(cluster_data)})")
        ax.set_title("Traction Trajectory by Cluster", fontsize=12, fontweight='bold')
    elif view == "Full Sample":
        mean_traj = wide_df[period_cols].mean()
        std_traj = wide_df[period_cols].std()
        ax.plot(periods, mean_traj, 'o-', linewidth=2.5, markersize=8, color='#2E86AB', label="Full Sample Mean")
        ax.fill_between(periods, mean_traj - std_traj, mean_traj + std_traj, alpha=0.2, color='#2E86AB', label="±1 SD")
        ax.set_title("Full Sample Traction Trajectory", fontsize=12, fontweight='bold')

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

# ═══════════════════════════════════════════════════════════════════════
# CALLBACKS
# ═══════════════════════════════════════════════════════════════════════

def handle_upload(change):
    global state
    if not file_in.value:
        return
    try:
        uploaded = list(file_in.value.values())[0]
        content = uploaded['content']
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

        html = df.head(10).to_html(index=False, border=0, max_rows=10)
        styled_html = f"""
        <div style="overflow-x:auto; max-width:100%; border:1px solid #ddd; border-radius:4px;">
            <style>
                .table {{ font-family: 'Courier New', monospace; font-size: 12px; border-collapse: collapse; }}
                .table th {{ background-color: #f5f5f5; padding: 8px 12px; text-align: left; border-bottom: 2px solid #ddd; white-space: nowrap; }}
                .table td {{ padding: 6px 12px; border-bottom: 1px solid #eee; white-space: nowrap; }}
                .table tr:hover {{ background-color: #f9f9f9; }}
            </style>
            {html}
        </div>
        """

        with preview_output:
            clear_output()
            display(HTML("<h4>Data Preview (first 10 rows)</h4>"))
            display(HTML(styled_html))

        stats_lines = [
            f"📊 Rows: {len(df):,}",
            f"📊 Columns: {len(df.columns)}",
            f"📊 Unique accounts: {df[likely_account[0]].nunique() if likely_account else 'N/A'}",
            f"📊 Periods: {sorted(df[likely_period[0]].unique()) if likely_period else 'N/A'}",
            f"📊 Numeric: {len(df.select_dtypes(include=[np.number]).columns)}",
            f"📊 Categorical/object: {len(df.select_dtypes(include=['object', 'category']).columns)}",
            "",
            "Column breakdown:"
        ]
        for col in cols:
            dtype = str(df[col].dtype)
            n_unique = df[col].nunique()
            stats_lines.append(f"  • {col}: {dtype} | {n_unique} unique")

        desc_stats.value = "\n".join(stats_lines)
        status.value = f"<p style='color:green;'>✅ Loaded: <b>{len(df):,}</b> rows × {len(df.columns)} columns</p>"

    except Exception as e:
        status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"
        with preview_output:
            clear_output()
            display(HTML(f"<p style='color:red;'>Error: {str(e)}</p>"))

def handle_configure(b):
    global state
    df = state['df_raw']
    ac = account_dropdown.value
    pc = period_dropdown.value

    if ac == pc:
        config_status.value = "<p style='color:red;'>❌ Account and Period must be different.</p>"
        return

    # ── NEW: Auto dummy-encode non-numeric columns ─────────────────────
    # Identify columns that are NOT account, NOT period, and NOT numeric
    non_numeric_cols = [c for c in df.columns if c not in [ac, pc] and not pd.api.types.is_numeric_dtype(df[c])]

    df_processed = df.copy()
    dummy_cols = []
    skipped_cols = []

    for col in non_numeric_cols:
        n_unique = df_processed[col].nunique()
        # Only dummy-encode if reasonable cardinality (≤20 categories) and not all unique (like an ID)
        if n_unique <= 20 and n_unique > 1 and n_unique < len(df_processed) * 0.9:
            dummies = pd.get_dummies(df_processed[col], prefix=col, drop_first=False)
            df_processed = pd.concat([df_processed, dummies], axis=1)
            dummy_cols.extend(dummies.columns.tolist())
        else:
            skipped_cols.append(f"{col} ({n_unique} unique)")

    # Now numeric_cols includes original numeric + dummy columns
    numeric_cols = [c for c in df_processed.columns if c not in [ac, pc] and pd.api.types.is_numeric_dtype(df_processed[c])]

    state['df_processed'] = df_processed
    state['account_col'] = ac
    state['period_col'] = pc
    state['numeric_cols'] = numeric_cols
    state['dummy_cols'] = dummy_cols

    if len(state['numeric_cols']) < 2:
        config_status.value = "<p style='color:red;'>❌ Need at least 2 numeric variables (original or dummy-encoded) for traction mapping.</p>"
        return

    n_accounts = df[ac].nunique()
    n_periods = df[pc].nunique()

    skip_msg = f"<br>Skipped: {', '.join(skipped_cols)}" if skipped_cols else ""
    config_status.value = f"<p style='color:green;'>✅ Panel configured: <b>{n_accounts:,}</b> accounts × <b>{n_periods:,}</b> periods. <b>{len(numeric_cols)}</b> numeric variables ({len(numeric_cols) - len(dummy_cols)} original + {len(dummy_cols)} dummies).{skip_msg}</p>"

    value_check.options = state['numeric_cols']
    value_check.value = ()
    value_check.disabled = False
    access_check.options = state['numeric_cols']
    access_check.value = ()
    access_check.disabled = False
    evidence_check.options = state['numeric_cols']
    evidence_check.value = ()
    evidence_check.disabled = False

    mapping_status.value = f"<p style='color:green;'>✅ <b>{len(state['numeric_cols'])}</b> variables available ({len(numeric_cols) - len(dummy_cols)} original numeric + {len(dummy_cols)} dummy-encoded). Select for each component.</p>"
    run_btn.disabled = False

    tabs.selected_index = 1

def update_weight_editor(change):
    global state
    cols = state['numeric_cols']
    if not cols:
        return
    value_vars = list(value_check.value)
    access_vars = list(access_check.value)
    evidence_vars = list(evidence_check.value)
    weight_editor.value = build_weight_text(value_vars, access_vars, evidence_vars)

def handle_clear_weights(b):
    weight_editor.value = ''
    value_check.value = ()
    access_check.value = ()
    evidence_check.value = ()

def handle_compute(b):
    global state
    df = state['df_processed']
    ac = state['account_col']
    pc = state['period_col']
    weight_text = weight_editor.value
    k = k_slider.value

    if df is None:
        run_status.value = "<p style='color:red;'>❌ Configure panel in Tab 1 first.</p>"
        return

    weights = parse_weights(weight_text)
    if not weights:
        run_status.value = "<p style='color:red;'>❌ Set weights in Tab 2 first.</p>"
        return

    value_vars = [v for v, w in weights.items() if w.get("Value", 0) > 0]
    access_vars = [v for v, w in weights.items() if w.get("Access", 0) > 0]
    evidence_vars = [v for v, w in weights.items() if w.get("Evidence", 0) > 0]

    if not value_vars or not access_vars or not evidence_vars:
        run_status.value = "<p style='color:red;'>❌ Each component needs at least one variable with weight > 0.</p>"
        return

    try:
        numeric_cols = state['numeric_cols']
        df_norm = df.copy()
        for col in numeric_cols:
            col_min = df[col].min()
            col_max = df[col].max()
            if col_max > col_min:
                df_norm[col] = (df[col] - col_min) / (col_max - col_min)
            else:
                df_norm[col] = 0.5

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

        # ── Wide format: FIX — handle unbalanced panel with fillna, not dropna ──
        # First, ensure period column is string for safe pivot column naming
        scored_long_copy = scored_long.copy()
        scored_long_copy[pc] = scored_long_copy[pc].astype(str)

        wide = scored_long_copy.pivot(index=ac, columns=pc, values="Traction_quotient")
        wide.columns = [f"Period_{c}" for c in wide.columns]
        wide = wide.reset_index()
        period_cols = [c for c in wide.columns if c.startswith("Period_")]

        # DIAGNOSTIC: report panel balance
        n_accounts_total = wide[ac].nunique()
        n_periods_total = len(period_cols)
        n_complete = wide.dropna(subset=period_cols).shape[0]

        # Fill missing periods with column mean (matches Gradio behavior)
        if period_cols:
            col_means = wide[period_cols].mean()
            wide[period_cols] = wide[period_cols].fillna(col_means)

        n_after_fill = len(wide)

        if n_after_fill < k:
            run_status.value = f"<p style='color:red;'>❌ Only {n_after_fill:,} accounts, need ≥{k} for K={k}.</p>"
            return

        # Cluster
        X = wide[period_cols].values
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

        # Centroids with sizes
        cluster_sizes = wide["Cluster"].value_counts().sort_index()
        centroids_data = []
        for i in range(k):
            cluster_data = wide[wide["Cluster"] == i]
            mean_traj = cluster_data[period_cols].mean()
            row = {"Cluster": f"Cluster {i+1}", "Size (n)": len(cluster_data)}
            for col in period_cols:
                row[col] = round(mean_traj[col], 4)
            centroids_data.append(row)
        centroids = pd.DataFrame(centroids_data)

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
        account_dropdown_view.disabled = False

        # Initial trajectory plot
        generate_trajectory_plot(wide, "Cluster Means", "(None)", k)

        diag_msg = f" Panel: {n_accounts_total} accounts × {n_periods_total} periods. {n_complete} complete before fill."
        run_status.value = f"<p style='color:green;'>✅ Computed traction for <b>{len(df):,}</b> rows. Clustered <b>{n_after_fill:,}</b> accounts into <b>{k}</b> trajectory clusters.{diag_msg}</p>"

        export_wide_btn.disabled = False
        export_long_btn.disabled = False
        export_report_btn.disabled = False
        export_status.value = "<p>Click export buttons to download results.</p>"

        tabs.selected_index = 2

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        run_status.value = f"<p style='color:red;'>❌ Error: {str(e)}<br><pre>{tb}</pre></p>"

def on_view_change(change):
    wide = state['scored_wide']
    k = state['k']
    if wide is not None:
        generate_trajectory_plot(wide, view_dropdown.value, account_dropdown_view.value, k)

def on_account_change(change):
    wide = state['scored_wide']
    k = state['k']
    if wide is not None:
        generate_trajectory_plot(wide, view_dropdown.value, account_dropdown_view.value, k)

def handle_export_wide(b):
    wide = state['scored_wide']
    if wide is None:
        export_status.value = "<p style='color:red;'>❌ Compute traction first.</p>"
        return
    path = "/tmp/panel_traction_wide.csv"
    wide.to_csv(path, index=False)
    export_status.value = f"<p style='color:green;'>✅ Wide format saved: {path} — Run <code>from google.colab import files; files.download('{path}')</code> to download</p>"

def handle_export_long(b):
    long = state['scored_long']
    if long is None:
        export_status.value = "<p style='color:red;'>❌ Compute traction first.</p>"
        return
    path = "/tmp/panel_traction_long.csv"
    long.to_csv(path, index=False)
    export_status.value = f"<p style='color:green;'>✅ Long format saved: {path} — Run <code>from google.colab import files; files.download('{path}')</code> to download</p>"

def handle_export_report(b):
    wide = state['scored_wide']
    long = state['scored_long']
    reflection = reflection_box.value
    k = state['k']

    if wide is None:
        export_status.value = "<p style='color:red;'>❌ Compute traction first.</p>"
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cluster_sizes = wide["Cluster"].value_counts().sort_index()

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
        size = cluster_sizes.get(i, 0)
        report.append(f"  Cluster {i+1}: {size} accounts ({size/len(wide)*100:.1f}%)")

    report.extend(["", "---", "", "## Reflection", "", reflection if reflection else "(No reflection provided)", "", "---", "", "*End of Report*"])

    path = "/tmp/panel_traction_report.txt"
    with open(path, "w") as f:
        f.write("\n".join(report))

    export_status.value = f"<p style='color:green;'>✅ Report saved: {path} — Run <code>from google.colab import files; files.download('{path}')</code> to download</p>"

# ── Wire up events ────────────────────────────────────────────────────
file_in.observe(handle_upload, names='value')
configure_btn.on_click(handle_configure)
value_check.observe(update_weight_editor, names='value')
access_check.observe(update_weight_editor, names='value')
evidence_check.observe(update_weight_editor, names='value')
clear_weights_btn.on_click(handle_clear_weights)
run_btn.on_click(handle_compute)
view_dropdown.observe(on_view_change, names='value')
account_dropdown_view.observe(on_account_change, names='value')
export_wide_btn.on_click(handle_export_wide)
export_long_btn.on_click(handle_export_long)
export_report_btn.on_click(handle_export_report)

# ── Display ───────────────────────────────────────────────────────────
display(widgets.HTML("<h1>📈 Panel Traction: Dynamic Account Scoring</h1>"))
display(widgets.HTML("<p><b>Upload panel data, compute monthly traction, cluster trajectories, and visualize dynamics.</b></p>"))
display(tabs)
