# ═══════════════════════════════════════════════════════════════════════
# MTGT Lec03: Competitor Traction Estimator (ipywidgets)
# Prompt 3 — Phase 4 Refinement: Vulnerability Score + Traction Model Toggle
# Paste into ONE Jupyter/Colab cell and run
# ═══════════════════════════════════════════════════════════════════════

# ── Quiet install ─────────────────────────────────────────────────────
import subprocess, sys
for pkg in ["ipywidgets", "pandas", "matplotlib", "IPython"]:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg])

# ── Imports ─────────────────────────────────────────────────────────────
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import warnings
warnings.filterwarnings('ignore')

# ── Global State ────────────────────────────────────────────────────────
state = {
    'df_raw': None,
    'df_configured': None,
    'df_normalized': None,
    'df_scored': None,
    'metric_meta': {},
    'metric_weights': {},
    'normalized_weights': {},
    'firm_col': None,
}

# ═══════════════════════════════════════════════════════════════════════
# PHASE 1: DATA INGESTION & PREVIEW
# ═══════════════════════════════════════════════════════════════════════

file_in = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='📁 Upload CSV',
    layout=widgets.Layout(width='200px')
)

status = widgets.HTML(value="<p style='color:#888;'>Upload a Feature Parity CSV to begin...</p>")
preview_output = widgets.Output()
with preview_output:
    display(HTML("<p style='color:#888;'>Upload CSV to see preview.</p>"))

info_box = widgets.HTML(value="<p><b>Dataset info will appear here.</b></p>")

phase1_box = widgets.VBox([
    widgets.HTML("<h2>📁 Phase 1: Upload Feature Parity Matrix</h2>"),
    widgets.HTML("<p>Upload a CSV where <b>rows = firms</b> and <b>columns = metrics/dimensions</b>. The first column should be the firm name.</p>"),
    widgets.HBox([file_in, status]),
    widgets.HTML("<h4>Data Preview</h4>"),
    preview_output,
    info_box
])

# ═══════════════════════════════════════════════════════════════════════
# PHASE 2: METRIC CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

config_vbox = widgets.VBox([])
config_status = widgets.HTML(value="<p>Upload data in Phase 1 first.</p>")
apply_config_btn = widgets.Button(
    description='✅ Apply Configuration',
    button_style='primary',
    layout=widgets.Layout(width='180px'),
    disabled=True
)

config_summary_output = widgets.Output()
with config_summary_output:
    display(HTML("<p style='color:#888;'>Configure metrics to see summary.</p>"))

phase2_box = widgets.VBox([
    widgets.HTML("<h2>🔧 Phase 2: Configure Each Metric</h2>"),
    widgets.HTML("<p>Set <b>Direction</b> (higher/lower is better) and <b>Pillar</b> for each metric. <code>Ignore</code> excludes it. <code>Switching</code> is used for vulnerability analysis, not Traction.</p>"),
    config_vbox,
    widgets.HBox([apply_config_btn, config_status]),
    widgets.HTML("<h4>Configuration Summary</h4>"),
    config_summary_output
])

# ═══════════════════════════════════════════════════════════════════════
# PHASE 3: WEIGHTING
# ═══════════════════════════════════════════════════════════════════════

weight_vbox = widgets.VBox([])
weight_status = widgets.HTML(value="<p>Apply configuration in Phase 2 first.</p>")
apply_weights_btn = widgets.Button(
    description='✅ Apply Weights',
    button_style='primary',
    layout=widgets.Layout(width='180px'),
    disabled=True
)

pillar_totals_html = widgets.HTML(value="<p>Pillar totals will appear here.</p>")
weight_summary_output = widgets.Output()
with weight_summary_output:
    display(HTML("<p style='color:#888;'>Set weights to see summary.</p>"))

phase3_box = widgets.VBox([
    widgets.HTML("<h2>⚖️ Phase 3: Weight Each Metric</h2>"),
    widgets.HTML("<p>Assign <b>Importance Weight</b> (0–5) per metric. Weights normalize within-pillar. Weight = 0 excludes the metric.</p>"),
    weight_vbox,
    widgets.HBox([apply_weights_btn, weight_status]),
    widgets.HTML("<h4>Live Pillar Weight Totals</h4>"),
    pillar_totals_html,
    widgets.HTML("<h4>Weight Summary</h4>"),
    weight_summary_output
])

# ═══════════════════════════════════════════════════════════════════════
# PHASE 4: SCORE COMPUTATION + VULNERABILITY
# ═══════════════════════════════════════════════════════════════════════

# Traction model toggle
traction_model = widgets.Dropdown(
    options=[('Multiplicative (A×V×E)', 'multiplicative'), ('Weighted Sum', 'weighted_sum')],
    value='multiplicative',
    description='Traction Model:',
    layout=widgets.Layout(width='280px')
)

vuln_method = widgets.Dropdown(
    options=[('Traction Gap × Switching', 'gap_x_switching'), ('Traction Gap only', 'gap_only'), ('Switching Friction only', 'switching_only')],
    value='gap_x_switching',
    description='Vulnerability:',
    layout=widgets.Layout(width='280px')
)

compute_btn = widgets.Button(
    description='📊 Compute Traction & Vulnerability',
    button_style='success',
    layout=widgets.Layout(width='250px'),
    disabled=True
)
compute_status = widgets.HTML(value="<p>Set weights in Phase 3 first.</p>")

scores_output = widgets.Output()
with scores_output:
    display(HTML("<p style='color:#888;'>Compute scores to see results.</p>"))

phase4_box = widgets.VBox([
    widgets.HTML("<h2>📊 Phase 4: Compute Traction & Vulnerability</h2>"),
    widgets.HTML("<p>Choose how Traction Proxy is computed and how Vulnerability is defined.</p>"),
    widgets.HBox([traction_model, vuln_method]),
    widgets.HBox([compute_btn, compute_status]),
    widgets.HTML("<h4>Competitor Scores & Rankings</h4>"),
    scores_output
])

# ═══════════════════════════════════════════════════════════════════════
# ASSEMBLE TABS
# ═══════════════════════════════════════════════════════════════════════

tabs = widgets.Tab(children=[phase1_box, phase2_box, phase3_box, phase4_box])
tabs.set_title(0, '📁 Upload & Preview')
tabs.set_title(1, '🔧 Configure Metrics')
tabs.set_title(2, '⚖️ Weight Metrics')
tabs.set_title(3, '📊 Compute Scores')

# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def identify_firm_column(df):
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]) or df[col].dtype == 'object':
            if df[col].nunique() >= min(2, len(df)) and df[col].nunique() <= len(df):
                return col
    return df.columns[0]

def handle_upload(change):
    global state
    if not file_in.value:
        return
    try:
        uploaded = list(file_in.value.values())[0]
        content = uploaded['content']
        df = pd.read_csv(io.BytesIO(content))
        state['df_raw'] = df

        firm_col = identify_firm_column(df)
        state['firm_col'] = firm_col

        html = df.to_html(index=False, border=0)
        styled = f"""
        <div style="overflow-x:auto; max-width:100%; border:1px solid #ddd; border-radius:4px; padding:8px;">
            <style>
                .table {{ font-family: 'Courier New', monospace; font-size: 11px; border-collapse: collapse; }}
                .table th {{ background-color: #e8f4f8; padding: 6px 10px; text-align: left; border-bottom: 2px solid #ddd; }}
                .table td {{ padding: 5px 10px; border-bottom: 1px solid #eee; }}
                .table tr:hover {{ background-color: #f9f9f9; }}
            </style>
            {html}
        </div>
        """
        with preview_output:
            clear_output()
            display(HTML(styled))

        numeric_cols = [c for c in df.columns if c != firm_col and pd.api.types.is_numeric_dtype(df[c])]
        info = f"""
        <p><b>✅ Loaded:</b> {len(df)} firms × {len(df.columns)} columns</p>
        <p><b>Firm column:</b> <code>{firm_col}</code></p>
        <p><b>Numeric metrics:</b> {len(numeric_cols)}</p>
        <p><b>Firms:</b> {', '.join(df[firm_col].astype(str).tolist())}</p>
        """
        info_box.value = info
        status.value = "<p style='color:green;'>✅ CSV loaded successfully</p>"

        build_config_widgets(df, firm_col)
        apply_config_btn.disabled = False
        config_status.value = "<p style='color:green;'>Ready — configure each metric.</p>"

    except Exception as e:
        status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"

def build_config_widgets(df, firm_col):
    numeric_cols = [c for c in df.columns if c != firm_col and pd.api.types.is_numeric_dtype(df[c])]
    rows = []
    rows.append(widgets.HBox([
        widgets.HTML("<b>Metric</b>", layout=widgets.Layout(width='220px')),
        widgets.HTML("<b>Direction</b>", layout=widgets.Layout(width='150px')),
        widgets.HTML("<b>Pillar</b>", layout=widgets.Layout(width='150px')),
        widgets.HTML("<b>Sample</b>", layout=widgets.Layout(width='100px'))
    ]))
    for col in numeric_cols:
        sample_val = df[col].iloc[0] if len(df) > 0 else 'N/A'
        direction_dd = widgets.Dropdown(
            options=[('Higher is better', 'higher'), ('Lower is better', 'lower')],
            value='higher',
            layout=widgets.Layout(width='140px')
        )
        pillar_dd = widgets.Dropdown(
            options=['Access', 'Value', 'Evidence', 'Switching', 'Ignore'],
            value='Value',
            layout=widgets.Layout(width='130px')
        )
        direction_dd._metric_name = col
        pillar_dd._metric_name = col
        rows.append(widgets.HBox([
            widgets.HTML(f"<code>{col}</code>", layout=widgets.Layout(width='220px')),
            direction_dd,
            pillar_dd,
            widgets.HTML(f"<span style='color:#888;'>{sample_val}</span>", layout=widgets.Layout(width='100px'))
        ]))
    config_vbox.children = rows

def handle_apply_config(b):
    global state
    df = state['df_raw']
    firm_col = state['firm_col']
    if df is None:
        config_status.value = "<p style='color:red;'>❌ Upload data first.</p>"
        return

    meta = {}
    for row in config_vbox.children[1:]:
        col_name = row.children[0].value.replace('<code>', '').replace('</code>', '')
        direction = row.children[1].value
        pillar = row.children[2].value
        meta[col_name] = {'direction': direction, 'pillar': pillar}

    state['metric_meta'] = meta

    df_cfg = df.copy()
    for col, settings in meta.items():
        if settings['direction'] == 'lower':
            cmin, cmax = df_cfg[col].min(), df_cfg[col].max()
            if cmax > cmin:
                df_cfg[col + '_reversed'] = cmax - df_cfg[col] + cmin
            else:
                df_cfg[col + '_reversed'] = df_cfg[col]

    state['df_configured'] = df_cfg

    summary_lines = ["<h4>Metric Configuration Summary</h4>", "<table style='font-size:12px; border-collapse:collapse;'>",
                     "<tr style='background:#e8f4f8;'><th>Metric</th><th>Direction</th><th>Pillar</th></tr>"]
    for col, settings in meta.items():
        rev_tag = " ↩️ reversed" if settings['direction'] == 'lower' else ""
        summary_lines.append(f"<tr><td><code>{col}</code>{rev_tag}</td><td>{settings['direction']}</td><td>{settings['pillar']}</td></tr>")
    summary_lines.append("</table>")

    with config_summary_output:
        clear_output()
        display(HTML("".join(summary_lines)))

    config_status.value = f"<p style='color:green;'>✅ {len(meta)} metrics configured.</p>"
    build_weight_widgets(meta)
    apply_weights_btn.disabled = False
    weight_status.value = "<p style='color:green;'>Ready — set weights.</p>"
    tabs.selected_index = 2

def build_weight_widgets(meta):
    rows = []
    rows.append(widgets.HBox([
        widgets.HTML("<b>Metric</b>", layout=widgets.Layout(width='220px')),
        widgets.HTML("<b>Pillar</b>", layout=widgets.Layout(width='100px')),
        widgets.HTML("<b>Weight (0–5)</b>", layout=widgets.Layout(width='200px')),
        widgets.HTML("<b>Value</b>", layout=widgets.Layout(width='60px'))
    ]))

    for col, settings in meta.items():
        if settings['pillar'] == 'Ignore':
            continue
        slider = widgets.FloatSlider(value=1.0, min=0.0, max=5.0, step=0.5, description='', layout=widgets.Layout(width='180px'))
        slider._metric_name = col
        slider._pillar = settings['pillar']
        slider.observe(update_pillar_totals, names='value')
        rows.append(widgets.HBox([
            widgets.HTML(f"<code>{col}</code>", layout=widgets.Layout(width='220px')),
            widgets.HTML(f"<span style='color:#666;'>{settings['pillar']}</span>", layout=widgets.Layout(width='100px')),
            slider,
            widgets.HTML("<span class='wval'>1.0</span>", layout=widgets.Layout(width='60px'))
        ]))

    weight_vbox.children = rows
    update_pillar_totals(None)

def update_pillar_totals(change):
    if not weight_vbox.children:
        return
    pillar_sums = {'Access': 0.0, 'Value': 0.0, 'Evidence': 0.0, 'Switching': 0.0}
    for row in weight_vbox.children[1:]:
        pillar = row.children[1].value.replace("<span style='color:#666;'>", "").replace("</span>", "")
        weight = row.children[2].value
        row.children[3].value = f"<span class='wval'>{weight:.1f}</span>"
        if pillar in pillar_sums:
            pillar_sums[pillar] += weight

    status_lines = ["<table style='font-size:13px;'>"]
    warnings = []
    for pillar, total in pillar_sums.items():
        color = "green" if total > 0 else "red"
        if total == 0:
            warnings.append(f"⚠️ <b>{pillar}</b> has zero weight")
        status_lines.append(f"<tr><td><b>{pillar}</b></td><td style='color:{color}; font-weight:bold;'>Σ = {total:.1f}</td></tr>")
    status_lines.append("</table>")
    if warnings:
        status_lines.append("<p style='color:orange;'>" + "<br>".join(warnings) + "</p>")
    pillar_totals_html.value = "".join(status_lines)

def handle_apply_weights(b):
    global state
    meta = state['metric_meta']
    if not meta:
        weight_status.value = "<p style='color:red;'>❌ Configure metrics first.</p>"
        return

    weights = {}
    for row in weight_vbox.children[1:]:
        col_name = row.children[0].value.replace('<code>', '').replace('</code>', '')
        weights[col_name] = row.children[2].value
    state['metric_weights'] = weights

    # Normalize within pillar
    pillar_weights = {'Access': {}, 'Value': {}, 'Evidence': {}, 'Switching': {}}
    for col, w in weights.items():
        pillar = meta[col]['pillar']
        if pillar != 'Ignore' and w > 0:
            pillar_weights[pillar][col] = w

    normalized = {}
    for pillar, wdict in pillar_weights.items():
        total = sum(wdict.values())
        if total > 0:
            for col, w in wdict.items():
                normalized[col] = w / total
        else:
            for col in wdict:
                normalized[col] = 0.0
    state['normalized_weights'] = normalized

    summary_lines = ["<h4>Normalized Weights (within-pillar)</h4>", "<table style='font-size:12px;'>"]
    summary_lines.append("<tr style='background:#e8f4f8;'><th>Metric</th><th>Pillar</th><th>Raw</th><th>Normalized</th></tr>")
    for col in sorted(weights.keys()):
        pillar = meta[col]['pillar']
        raw = weights[col]
        norm = normalized.get(col, 0.0)
        summary_lines.append(f"<tr><td><code>{col}</code></td><td>{pillar}</td><td>{raw:.1f}</td><td><b>{norm:.3f}</b></td></tr>")
    summary_lines.append("</table>")

    with weight_summary_output:
        clear_output()
        display(HTML("".join(summary_lines)))

    weight_status.value = "<p style='color:green;'>✅ Weights applied.</p>"
    compute_btn.disabled = False
    compute_status.value = "<p style='color:green;'>Ready to compute.</p>"
    tabs.selected_index = 3

def handle_compute(b):
    global state
    df = state['df_configured']
    firm_col = state['firm_col']
    meta = state['metric_meta']
    weights = state.get('normalized_weights', {})
    model = traction_model.value
    vuln = vuln_method.value

    if df is None or not meta:
        compute_status.value = "<p style='color:red;'>❌ Apply config and weights first.</p>"
        return

    try:
        # Normalize metrics to 0-1
        df_norm = df.copy()
        active_metrics = []

        for col, settings in meta.items():
            if settings['pillar'] == 'Ignore':
                continue
            if weights.get(col, 0) == 0:
                continue

            eff_col = col + '_reversed' if settings['direction'] == 'lower' else col
            cmin, cmax = df_norm[eff_col].min(), df_norm[eff_col].max()
            if cmax > cmin:
                df_norm[col + '_norm'] = (df_norm[eff_col] - cmin) / (cmax - cmin)
            else:
                df_norm[col + '_norm'] = 0.5
            active_metrics.append((col, col + '_norm', settings['pillar'], weights[col]))

        state['df_normalized'] = df_norm

        # Compute scores per firm
        results = []
        for idx, row in df_norm.iterrows():
            firm_name = row[firm_col]

            # Weighted pillar scores
            access_wsum = access_wtotal = 0
            value_wsum = value_wtotal = 0
            evidence_wsum = evidence_wtotal = 0
            switching_wsum = switching_wtotal = 0

            for col, norm_col, pillar, weight in active_metrics:
                val = row[norm_col]
                if pillar == 'Access':
                    access_wsum += val * weight; access_wtotal += weight
                elif pillar == 'Value':
                    value_wsum += val * weight; value_wtotal += weight
                elif pillar == 'Evidence':
                    evidence_wsum += val * weight; evidence_wtotal += weight
                elif pillar == 'Switching':
                    switching_wsum += val * weight; switching_wtotal += weight

            access_score = access_wsum / access_wtotal if access_wtotal > 0 else 0
            value_score = value_wsum / value_wtotal if value_wtotal > 0 else 0
            evidence_score = evidence_wsum / evidence_wtotal if evidence_wtotal > 0 else 0
            switching_score = switching_wsum / switching_wtotal if switching_wtotal > 0 else 0

            # Traction Proxy based on model
            if model == 'multiplicative':
                traction_proxy = access_score * value_score * evidence_score
            else:  # weighted_sum
                # Average of the three pillar scores (equal pillars)
                traction_proxy = (access_score + value_score + evidence_score) / 3

            results.append({
                firm_col: firm_name,
                'Access_Score': round(access_score, 4),
                'Value_Score': round(value_score, 4),
                'Evidence_Score': round(evidence_score, 4),
                'Switching_Score': round(switching_score, 4),
                'Traction_Proxy': round(traction_proxy, 4)
            })

        df_scored = pd.DataFrame(results)

        # ── VULNERABILITY ANALYSIS ──
        # Find DevSuite reference
        devsuite_row = df_scored[df_scored[firm_col].str.contains('DevSuite', case=False, na=False)]
        if len(devsuite_row) == 0:
            # Fallback: use highest traction as reference
            devsuite_traction = df_scored['Traction_Proxy'].max()
            devsuite_switching = df_scored['Switching_Score'].mean()
        else:
            devsuite_traction = devsuite_row['Traction_Proxy'].values[0]
            devsuite_switching = devsuite_row['Switching_Score'].values[0]

        # Compute vulnerability for each competitor
        vuln_scores = []
        for _, r in df_scored.iterrows():
            firm = r[firm_col]
            traction_gap = max(0, devsuite_traction - r['Traction_Proxy'])  # how far below DevSuite
            switching = r['Switching_Score']

            if vuln == 'gap_x_switching':
                vuln_score = traction_gap * switching  # low traction + high switching = vulnerable
            elif vuln == 'gap_only':
                vuln_score = traction_gap
            else:  # switching_only
                vuln_score = switching

            vuln_scores.append({
                firm_col: firm,
                'Traction_Proxy': r['Traction_Proxy'],
                'Traction_Gap': round(traction_gap, 4),
                'Switching_Score': round(switching, 4),
                'Vulnerability_Score': round(vuln_score, 4)
            })

        df_vuln = pd.DataFrame(vuln_scores)
        df_vuln = df_vuln.sort_values('Vulnerability_Score', ascending=False).reset_index(drop=True)

        state['df_scored'] = df_scored
        state['df_vuln'] = df_vuln

        with scores_output:
            clear_output()

            # Traction Ranking
            df_sorted = df_scored.sort_values('Traction_Proxy', ascending=False).reset_index(drop=True)
            display(HTML("<h4>🏆 Traction Proxy Ranking</h4>"))
            rank_html = "<ol>"
            for _, r in df_sorted.iterrows():
                rank_html += f"<li><b>{r[firm_col]}</b>: Traction = {r['Traction_Proxy']:.4f} (A={r['Access_Score']:.3f}, V={r['Value_Score']:.3f}, E={r['Evidence_Score']:.3f})</li>"
            rank_html += "</ol>"
            display(HTML(rank_html))

            # Vulnerability Ranking
            display(HTML("<h4>🎯 Vulnerability Ranking (Most Vulnerable First)</h4>"))
            vuln_html = "<ol>"
            for _, r in df_vuln.iterrows():
                is_devsuite = 'DevSuite' in str(r[firm_col])
                highlight = " <span style='color:green; font-weight:bold;'>(YOU)</span>" if is_devsuite else ""
                vuln_html += f"<li><b>{r[firm_col]}</b>{highlight}: Vuln = {r['Vulnerability_Score']:.4f} (Gap={r['Traction_Gap']:.3f}, Switching={r['Switching_Score']:.3f})</li>"
            vuln_html += "</ol>"
            display(HTML(vuln_html))

            # Full table
            display(HTML("<h4>📊 Full Score Table</h4>"))
            display_cols = [firm_col, 'Access_Score', 'Value_Score', 'Evidence_Score', 'Switching_Score', 'Traction_Proxy']
            display(df_scored[display_cols].style.set_properties(**{'font-size': '11px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#e8f4f8'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]).background_gradient(subset=['Traction_Proxy'], cmap='RdYlGn'))

            # Bar chart
            fig, ax = plt.subplots(figsize=(10, 5))
            x = np.arange(len(df_scored))
            width = 0.2
            ax.bar(x - 1.5*width, df_scored['Access_Score'], width, label='Access', color='#3498db')
            ax.bar(x - 0.5*width, df_scored['Value_Score'], width, label='Value', color='#2ecc71')
            ax.bar(x + 0.5*width, df_scored['Evidence_Score'], width, label='Evidence', color='#e74c3c')
            ax.bar(x + 1.5*width, df_scored['Traction_Proxy'], width, label='Traction Proxy', color='#9b59b6')
            ax.set_xticks(x)
            ax.set_xticklabels(df_scored[firm_col], rotation=15, ha='right')
            ax.set_ylabel('Score (0-1 scale)', fontsize=11)
            ax.set_title(f'Competitor Traction Scores ({"Multiplicative" if model == "multiplicative" else "Weighted Sum"})', fontsize=12, fontweight='bold')
            ax.legend(loc='best')
            ax.set_ylim(0, 1.05)
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            display(fig)
            plt.close(fig)

            # Vulnerability bar chart
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            colors = ['#e74c3c' if 'DevSuite' not in str(f) else '#2ecc71' for f in df_vuln[firm_col]]
            ax2.barh(df_vuln[firm_col], df_vuln['Vulnerability_Score'], color=colors)
            ax2.set_xlabel('Vulnerability Score', fontsize=11)
            ax2.set_title('Vulnerability Ranking (Higher = More Vulnerable to DevSuite)', fontsize=12, fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            display(fig2)
            plt.close(fig2)

        compute_status.value = f"<p style='color:green;'>✅ Computed for {len(df_scored)} firms. Model: {traction_model.label}. Vuln: {vuln_method.label}.</p>"

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        compute_status.value = f"<p style='color:red;'>❌ Error: {str(e)}<br><pre>{tb}</pre></p>"

# ── Wire up ───────────────────────────────────────────────────────────
file_in.observe(handle_upload, names='value')
apply_config_btn.on_click(handle_apply_config)
apply_weights_btn.on_click(handle_apply_weights)
compute_btn.on_click(handle_compute)

# ── Display ───────────────────────────────────────────────────────────
display(widgets.HTML("<h1>📊 Competitor Traction Estimator</h1>"))
display(widgets.HTML("<p><b>Upload → Configure → Weight → Compute Traction & Vulnerability.</b></p>"))
display(tabs)
