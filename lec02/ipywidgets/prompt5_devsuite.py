# ═══════════════════════════════════════════════════════════════════════
# Generic Customer Segmentation & Traction Audit (ipywidgets V6)
# 6 tabs: Upload, Variables, Segmentation, Results, Traction Mapping, Traction Calculation
# FIXED: Individual row-level traction, transposed centroids, 4-decimal rounding, calc_btn early enable
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
from IPython.display import display, HTML, clear_output, FileLink
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from datetime import datetime
import io
import warnings
warnings.filterwarnings('ignore')

# ── Global State ────────────────────────────────────────────────────────
state = {
    'df_raw': None,
    'df_processed': None,
    'processed_vars': [],
    'X_scaled': None,
    'segment_labels': None,
    'segment_names': ["Segment 1", "Segment 2", "Segment 3"],
    'scored_df': None,
    'wcss': None,
    'ks': None,
    'k_value': 3
}

# ═══════════════════════════════════════════════════════════════════════
# TAB 1: DATA PREVIEW
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
    display(HTML("<p style='color:#888;'>Upload a CSV to see data preview.</p>"))

desc_stats = widgets.Textarea(
    value="Upload a CSV to see dataset summary.",
    description='Overview:',
    layout=widgets.Layout(width='100%', height='250px'),
    disabled=True
)

tab1 = widgets.VBox([
    widgets.HTML("<h2>📁 Data Preview</h2>"),
    widgets.HBox([file_in, status]),
    widgets.HTML("<h4>Raw Data Preview</h4>"),
    preview_output,
    widgets.HTML("<h4>Dataset Overview</h4>"),
    desc_stats
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 2: VARIABLE SELECTION
# ═══════════════════════════════════════════════════════════════════════

basis_check = widgets.SelectMultiple(
    options=['(Upload CSV first)'],
    value=(),
    description='Basis vars:',
    rows=8,
    layout=widgets.Layout(width='350px'),
    disabled=True
)

cat_check = widgets.SelectMultiple(
    options=['(Select basis variables first)'],
    value=(),
    description='Categorical:',
    rows=8,
    layout=widgets.Layout(width='350px'),
    disabled=True
)

summary = widgets.Textarea(
    value="Upload CSV and select variables to see summary.",
    description='Summary:',
    layout=widgets.Layout(width='100%', height='300px'),
    disabled=True
)

confirm_btn = widgets.Button(
    description='✅ Confirm & Create Dummies',
    button_style='primary',
    layout=widgets.Layout(width='220px'),
    disabled=True
)

confirm_status = widgets.HTML(value="<p>Select variables and click Confirm to prepare data.</p>")

tab2 = widgets.VBox([
    widgets.HTML("<h2>🔧 Variable Selection</h2>"),
    widgets.HTML("<h3>Configure Variables for Clustering</h3>"),
    widgets.HTML("<p><b>Step A:</b> Select basis variables to include in the analysis.</p>"),
    widgets.HBox([basis_check, widgets.VBox([
        widgets.HTML("<p><b>Step B:</b> From selected basis variables, check those needing dummy encoding.</p>"),
        cat_check
    ])]),
    widgets.HTML("<h4>Variable Summary</h4>"),
    summary,
    widgets.HBox([confirm_btn, confirm_status])
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 3: SEGMENTATION
# ═══════════════════════════════════════════════════════════════════════

scree_output = widgets.Output()
with scree_output:
    display(HTML("<p style='color:#888;'>Confirm variables in Tab 2 first to see scree plot.</p>"))

wcss_output = widgets.Output()
with wcss_output:
    display(HTML("<p style='color:#888;'>WCSS table will appear after confirming variables.</p>"))

k_slider = widgets.IntSlider(value=3, min=2, max=10, step=1, description='K:', layout=widgets.Layout(width='300px'))

run_btn = widgets.Button(
    description='▶️ Run Segmentation',
    button_style='success',
    layout=widgets.Layout(width='180px'),
    disabled=True
)

seg_status = widgets.HTML(value="<p>Confirm variables in Tab 2 first.</p>")

tab3 = widgets.VBox([
    widgets.HTML("<h2>🎯 Segmentation</h2>"),
    widgets.HTML("<h3>K-Means Clustering</h3>"),
    widgets.HTML("<p><b>Step 1:</b> Review the scree plot below. The elbow suggests optimal K.</p>"),
    widgets.HBox([scree_output, widgets.VBox([
        widgets.HTML("<p><b>WCSS Values</b></p>"),
        wcss_output
    ])]),
    widgets.HTML("<p><b>Step 2:</b> Choose K and run segmentation.</p>"),
    widgets.HBox([k_slider, run_btn, seg_status])
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 4: RESULTS + SEGMENT NAMING
# ═══════════════════════════════════════════════════════════════════════

segment_names_input = widgets.Textarea(
    value='Segment 1, Segment 2, Segment 3',
    description='Names:',
    layout=widgets.Layout(width='400px', height='60px')
)

apply_names_btn = widgets.Button(
    description='✏️ Apply Names',
    button_style='info',
    layout=widgets.Layout(width='120px'),
    disabled=True
)

names_status = widgets.HTML(value="<p>Run segmentation first, then name your segments.</p>")

sizes_output = widgets.Output()
with sizes_output:
    display(HTML("<p style='color:#888;'>Run segmentation in Tab 3 to see segment sizes.</p>"))

cents_output = widgets.Output()
with cents_output:
    display(HTML("<p style='color:#888;'>Run segmentation in Tab 3 to see centroids.</p>"))

scatter_output = widgets.Output()
with scatter_output:
    display(HTML("<p style='color:#888;'>Run segmentation in Tab 3 to see PCA scatter.</p>"))

labeled_output = widgets.Output()
with labeled_output:
    display(HTML("<p style='color:#888;'>Run segmentation in Tab 3 to see labeled data.</p>"))

tab4 = widgets.VBox([
    widgets.HTML("<h2>📊 Results</h2>"),
    widgets.HTML("<h3>Segmentation Results</h3>"),
    widgets.HTML("<h4>Name Your Segments</h4>"),
    widgets.HTML("<p><i>Enter custom names below (comma-separated, in order). Default: Segment 1, Segment 2, ...</i></p>"),
    widgets.HBox([segment_names_input, apply_names_btn, names_status]),
    widgets.HTML("<h4>Segment Sizes & Centroids</h4>"),
    widgets.HBox([sizes_output, cents_output]),
    widgets.HTML("<h4>PCA Scatter Plot</h4>"),
    scatter_output,
    widgets.HTML("<h4>Segmented Data Preview</h4>"),
    labeled_output
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 5: TRACTION MAPPING + REFLECTION (FIXED: reflection moved here)
# ═══════════════════════════════════════════════════════════════════════

value_check = widgets.SelectMultiple(
    options=['(Run segmentation first)'],
    value=(),
    description='Value:',
    rows=6,
    layout=widgets.Layout(width='250px'),
    disabled=True
)

access_check = widgets.SelectMultiple(
    options=['(Run segmentation first)'],
    value=(),
    description='Access:',
    rows=6,
    layout=widgets.Layout(width='250px'),
    disabled=True
)

evidence_check = widgets.SelectMultiple(
    options=['(Run segmentation first)'],
    value=(),
    description='Evidence:',
    rows=6,
    layout=widgets.Layout(width='250px'),
    disabled=True
)

# Reflection moved to Tab 5
reflection_box = widgets.Textarea(
    value='',
    placeholder='Why did you map these specific variables to Value/Access/Evidence? What trade-offs did you consider?',
    description='Reflection:',
    layout=widgets.Layout(width='100%', height='120px')
)

weight_editor = widgets.Textarea(
    value='',
    placeholder='variable=Component:weight (one per line)',
    description='Weights:',
    layout=widgets.Layout(width='500px', height='150px')
)

clear_weights_btn = widgets.Button(
    description='🔄 Clear All',
    button_style='warning',
    layout=widgets.Layout(width='100px')
)

mapping_status = widgets.HTML(value="<p>Run segmentation first, then select variables and set weights.</p>")

tab5 = widgets.VBox([
    widgets.HTML("<h2>🔧 Mapping Traction Components</h2>"),
    widgets.HTML("""
    <p><b>Step 1:</b> Check variables for each component. <b>Step 2:</b> Reflect on your mapping choices.
    <b>Step 3:</b> Set weights (0–1+). Weight = 0 excludes the variable. Weight > 0 includes it proportionally.</p>
    """),
    widgets.HTML("<p><b>Step 1: Select Variables per Component</b></p>"),
    widgets.HBox([value_check, access_check, evidence_check]),
    widgets.HTML("<p><b>Step 2: 📝 Reflect on Your Mapping</b></p>"),
    widgets.HTML("<p><i>Why did you map these specific variables to Value/Access/Evidence? What trade-offs did you consider?</i></p>"),
    reflection_box,
    widgets.HTML("<p><b>Step 3: Set Weights for Selected Variables</b></p>"),
    widgets.HTML("<p><i>Format: <code>variable_name=Component:weight</code> one per line. Auto-populates from selections above with default weight=1.</i></p>"),
    widgets.HBox([weight_editor, widgets.VBox([clear_weights_btn])]),
    mapping_status
])

# ═══════════════════════════════════════════════════════════════════════
# TAB 6: TRACTION CALCULATION + INDIVIDUAL SCORING + EXPORT
# ═══════════════════════════════════════════════════════════════════════

calc_btn = widgets.Button(
    description='📊 Calculate Traction Quotient',
    button_style='success',
    layout=widgets.Layout(width='220px'),
    disabled=True
)

traction_status = widgets.HTML(value="<p>Configure mapping in Tab 5, then click Calculate.</p>")

overall_output = widgets.Output()
with overall_output:
    display(HTML("<p style='color:#888;'>Overall sample traction will appear after calculation.</p>"))

segment_output = widgets.Output()
with segment_output:
    display(HTML("<p style='color:#888;'>Segment-wise traction will appear after calculation.</p>"))

ranking_txt = widgets.Textarea(
    value='',
    description='Rankings:',
    layout=widgets.Layout(width='100%', height='200px'),
    disabled=True
)

# Individual scoring section
individual_output = widgets.Output()
with individual_output:
    display(HTML("<p style='color:#888;'>Individual-level scores will appear after calculation.</p>"))

traction_hist_output = widgets.Output()
with traction_hist_output:
    display(HTML("<p style='color:#888;'>Traction score distribution histogram will appear after calculation.</p>"))

export_report_btn = widgets.Button(
    description='📄 Download Report (TXT)',
    button_style='info',
    layout=widgets.Layout(width='180px'),
    disabled=True
)

export_csv_btn = widgets.Button(
    description='📊 Download Scored Data (CSV)',
    button_style='info',
    layout=widgets.Layout(width='200px'),
    disabled=True
)

export_status = widgets.HTML(value="<p>Calculate traction, then export.</p>")

tab6 = widgets.VBox([
    widgets.HTML("<h2>📊 Traction Calculation</h2>"),
    widgets.HTML("<h3>Traction Results</h3>"),
    widgets.HTML("<p><b>Overall Sample</b> (K=1, no clustering) vs <b>Segment-wise</b> (your named segments) + <b>Individual-level</b> scoring</p>"),
    widgets.HBox([calc_btn, traction_status]),
    widgets.HTML("<h4>Overall Sample (K=1 Baseline)</h4>"),
    overall_output,
    widgets.HTML("<h4>Segment-wise Traction (Transposed for AI Copy-Paste)</h4>"),
    segment_output,
    widgets.HTML("<h4>Segment Rankings</h4>"),
    ranking_txt,
    widgets.HTML("<h4>👤 Individual-Level Traction Scores</h4>"),
    widgets.HTML("<p><i>Each row gets its own Value, Access, Evidence, and Traction score.</i></p>"),
    individual_output,
    widgets.HTML("<h4>Traction Score Distribution by Segment</h4>"),
    traction_hist_output,
    widgets.HTML("<h4>📥 Export</h4>"),
    widgets.HBox([export_report_btn, export_csv_btn, export_status])
])

# ═══════════════════════════════════════════════════════════════════════
# ASSEMBLE TABS
# ═══════════════════════════════════════════════════════════════════════

tabs = widgets.Tab(children=[tab1, tab2, tab3, tab4, tab5, tab6])
tabs.set_title(0, '📁 Data Preview')
tabs.set_title(1, '🔧 Variable Selection')
tabs.set_title(2, '🎯 Segmentation')
tabs.set_title(3, '📊 Results')
tabs.set_title(4, '🔧 Traction Mapping')
tabs.set_title(5, '📊 Traction Calculation')

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

def parse_segment_names(names_text, k):
    if not names_text:
        return [f"Segment {i+1}" for i in range(k)]
    names = [n.strip() for n in names_text.split(",")]
    while len(names) < k:
        names.append(f"Segment {len(names)+1}")
    return names[:k]

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
        all_cols = df.columns.tolist()

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
            display(HTML("<h4>Raw Data Preview (first 10 rows)</h4>"))
            display(HTML(styled_html))

        stats_lines = [
            f"📊 Rows: {len(df):,}",
            f"📊 Columns: {len(df.columns)}",
            f"📊 Numeric: {len(df.select_dtypes(include=[np.number]).columns)}",
            f"📊 Categorical/object: {len(df.select_dtypes(include=['object', 'category']).columns)}",
            f"📊 Missing: {df.isnull().sum().sum():,} ({100*df.isnull().sum().sum()/(df.shape[0]*df.shape[1]):.1f}%)",
            "",
            "Column breakdown:"
        ]
        for col in all_cols:
            dtype = str(df[col].dtype)
            n_unique = df[col].nunique()
            n_missing = df[col].isnull().sum()
            stats_lines.append(f"  • {col}: {dtype} | {n_unique} unique | {n_missing} missing")

        desc_stats.value = "\n".join(stats_lines)
        status.value = f"<p style='color:green;'>✅ Loaded: <b>{len(df):,}</b> rows × {len(df.columns)} columns</p>"

        basis_check.options = all_cols
        basis_check.value = ()
        basis_check.disabled = False

        cat_check.options = ['(Select basis variables first)']
        cat_check.value = ()
        cat_check.disabled = True

        summary.value = "Upload CSV and select basis variables."
        confirm_status.value = "<p>Select variables and click Confirm to prepare data.</p>"
        confirm_btn.disabled = True
        run_btn.disabled = True
        seg_status.value = "<p>Confirm variables in Tab 2 first.</p>"

        with scree_output:
            clear_output()
            display(HTML("<p style='color:#888;'>Confirm variables in Tab 2 first to see scree plot.</p>"))
        with wcss_output:
            clear_output()
            display(HTML("<p style='color:#888;'>WCSS table will appear after confirming variables.</p>"))

        apply_names_btn.disabled = True
        names_status.value = "<p>Run segmentation first, then name your segments.</p>"
        value_check.options = ['(Run segmentation first)']
        value_check.value = ()
        value_check.disabled = True
        access_check.options = ['(Run segmentation first)']
        access_check.value = ()
        access_check.disabled = True
        evidence_check.options = ['(Run segmentation first)']
        evidence_check.value = ()
        evidence_check.disabled = True
        weight_editor.value = ''
        mapping_status.value = "<p>Run segmentation first, then select variables and set weights.</p>"
        calc_btn.disabled = True
        traction_status.value = "<p>Configure mapping in Tab 5, then click Calculate.</p>"
        export_report_btn.disabled = True
        export_csv_btn.disabled = True
        export_status.value = "<p>Calculate traction, then export.</p>"

    except Exception as e:
        status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"
        with preview_output:
            clear_output()
            display(HTML(f"<p style='color:red;'>Error: {str(e)}</p>"))

def handle_basis_change(change):
    global state
    if state['df_raw'] is None:
        return
    selected_basis = list(basis_check.value)
    if not selected_basis:
        cat_check.options = ['(Select basis variables first)']
        cat_check.value = ()
        cat_check.disabled = True
        summary.value = "Upload CSV and select basis variables."
        confirm_btn.disabled = True
        return
    cat_check.options = selected_basis
    cat_check.value = ()
    cat_check.disabled = False
    confirm_btn.disabled = False
    lines = [f"📊 Basis variables: {len(selected_basis)}"]
    for v in selected_basis:
        dtype = str(state['df_raw'][v].dtype)
        n_unique = state['df_raw'][v].nunique()
        lines.append(f"  • {v}: {dtype} | {n_unique} unique values")
    summary.value = "\n".join(lines)

def handle_cat_change(change):
    global state
    if state['df_raw'] is None:
        return
    selected_basis = list(basis_check.value)
    selected_cat = list(cat_check.value)
    if not selected_basis:
        summary.value = "Upload CSV and select basis variables."
        return
    numeric_vars = [v for v in selected_basis if v not in selected_cat]
    lines = [
        f"📊 Basis variables: {len(selected_basis)}",
        f"🔤 Categorical (dummy): {len(selected_cat)}",
        f"🔢 Numeric (direct): {len(numeric_vars)}",
        "",
        "Final variable list:"
    ]
    for v in selected_basis:
        marker = "🔤" if v in selected_cat else "🔢"
        dtype = str(state['df_raw'][v].dtype)
        lines.append(f"  {marker} {v} ({dtype})")
    if selected_cat:
        lines.append("")
        lines.append("Dummy variables to create (n-1, first category as base):")
        for v in selected_cat:
            n_cats = state['df_raw'][v].nunique()
            lines.append(f"  • {v}: {n_cats} categories → {n_cats - 1} dummies")
    summary.value = "\n".join(lines)

def handle_confirm(b):
    global state
    df = state['df_raw']
    selected_basis = list(basis_check.value)
    selected_cat = list(cat_check.value)
    if df is None or not selected_basis:
        confirm_status.value = "<p style='color:red;'>❌ Please select basis variables first.</p>"
        return
    try:
        df_proc = df[selected_basis].copy()
        df_proc = df_proc.dropna()
        if len(df_proc) < 2:
            confirm_status.value = "<p style='color:red;'>❌ Not enough valid rows after dropping missing values.</p>"
            return
        for col in selected_cat:
            if col in df_proc.columns:
                dummies = pd.get_dummies(df_proc[col], prefix=col, drop_first=True)
                dummies = dummies.astype(int)
                df_proc = pd.concat([df_proc.drop(columns=[col]), dummies], axis=1)
        non_numeric = df_proc.select_dtypes(exclude=[np.number]).columns.tolist()
        if non_numeric:
            confirm_status.value = f"<p style='color:red;'>❌ Non-numeric columns remain: {non_numeric}</p>"
            return
        final_cols = df_proc.columns.tolist()
        state['df_processed'] = df_proc
        state['processed_vars'] = final_cols

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_proc.values)
        state['X_scaled'] = X_scaled

        wcss = []
        ks = range(1, min(11, len(X_scaled)))
        for k in ks:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            wcss.append(km.inertia_)
        state['wcss'] = wcss
        state['ks'] = list(ks)

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(list(ks), wcss, 'o-', linewidth=2.5, markersize=9, color='#2E86AB')
        for i in range(1, len(wcss)):
            pct_drop = (wcss[i-1] - wcss[i]) / wcss[i-1] * 100
            ax.annotate(f"{pct_drop:.1f}%", xy=(i+1, wcss[i]), xytext=(5, 10),
                       textcoords='offset points', fontsize=8, color='#555', alpha=0.8)
        if len(wcss) > 2:
            drops = [(wcss[i-1] - wcss[i]) / wcss[i-1] * 100 for i in range(1, len(wcss))]
            best_k = drops.index(max(drops)) + 2
            ax.axvline(x=best_k, color='red', linestyle='--', alpha=0.5, label=f'Suggested K={best_k}')
            ax.legend()
        ax.set_xlabel('K (Number of Segments)', fontsize=12)
        ax.set_ylabel('WCSS (Standardized Data)', fontsize=12)
        ax.set_title('Scree Plot with % Drop Annotations', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(list(ks))
        plt.tight_layout()

        with scree_output:
            clear_output()
            display(fig)
        plt.close(fig)

        wcss_df = pd.DataFrame({"K": list(ks), "WCSS": [round(w, 4) for w in wcss]})
        pct_drops = [None] + [round((wcss[i-1] - wcss[i]) / wcss[i-1] * 100, 4) for i in range(1, len(wcss))]
        wcss_df["Pct_Drop"] = pct_drops

        with wcss_output:
            clear_output()
            display(HTML("<p><b>WCSS Values</b></p>"))
            display(wcss_df.style.set_properties(**{'font-size': '11px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#e8f4f8'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        confirm_status.value = f"<p style='color:green;'>✅ Standardized & dummies ready! <b>{len(df_proc):,}</b> rows × <b>{len(final_cols)}</b> columns.</p>"
        run_btn.disabled = False
        seg_status.value = "<p>Ready to run segmentation. Choose K and click Run.</p>"
        tabs.selected_index = 2
    except Exception as e:
        confirm_status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"

def handle_run(b):
    global state
    df_proc = state['df_processed']
    X_scaled = state['X_scaled']
    processed_cols = state['processed_vars']
    k = k_slider.value
    state['k_value'] = k

    if df_proc is None or X_scaled is None:
        seg_status.value = "<p style='color:red;'>❌ Confirm variables in Tab 2 first.</p>"
        return
    if len(X_scaled) < k:
        seg_status.value = f"<p style='color:red;'>❌ Need ≥{k} rows for K={k}.</p>"
        return
    try:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        state['segment_labels'] = labels

        default_names = [f"Segment {i+1}" for i in range(k)]
        state['segment_names'] = default_names
        segment_names_input.value = ", ".join(default_names)

        # Enable calc_btn IMMEDIATELY after successful segmentation (before any display)
        calc_btn.disabled = False

        # Transposed centroids — 4 decimal rounding
        cents = pd.DataFrame(
            np.round(km.cluster_centers_, 4).T,
            index=processed_cols,
            columns=default_names
        )
        cents.index.name = "Variable"
        cents = cents.reset_index()

        sizes = pd.Series(labels).value_counts().sort_index()
        sizes_df = pd.DataFrame({
            "Segment": [default_names[i] for i in sizes.index],
            "Count": sizes.values,
            "Pct": (sizes.values / len(labels) * 100).round(4)
        })

        pca = PCA(n_components=2)
        Xp = pca.fit_transform(X_scaled)

        fig, ax = plt.subplots(figsize=(9, 6))
        colors = plt.cm.Set2(np.linspace(0, 1, k))
        for i in range(k):
            mask = labels == i
            ax.scatter(Xp[mask, 0], Xp[mask, 1], c=[colors[i]],
                       label=default_names[i], alpha=0.7, s=80,
                       edgecolors='white', linewidth=0.5)
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})", fontsize=11)
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})", fontsize=11)
        ax.set_title("Segment Scatter Plot (PCA of Standardized Data)", fontsize=14, fontweight='bold')
        ax.legend(title="Segments", loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        with scatter_output:
            clear_output()
            display(fig)
        plt.close(fig)

        with sizes_output:
            clear_output()
            display(HTML("<h4>Segment Sizes</h4>"))
            display(sizes_df.style.set_properties(**{'font-size': '11px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#e8f4f8'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        with cents_output:
            clear_output()
            display(HTML("<h4>Centroids (Standardized Scale, 4 decimals) — Transposed</h4>"))
            display(HTML("<p><i>Variables as rows, Segments as columns. Download CSV below for easy copy-paste into AI queries.</i></p>"))
            display(cents.style.set_properties(**{'font-size': '10px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#e8f4f8'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))
            # Downloadable CSV for copy-paste
            cents_csv_path = "/tmp/centroids.csv"
            cents.to_csv(cents_csv_path, index=False)
            display(HTML(f"<p><a href='{FileLink(cents_csv_path).href}' target='_blank'>📥 Download Centroids CSV</a></p>"))

        result_df = df_proc.copy()
        result_df["Segment"] = [default_names[l] for l in labels]

        with labeled_output:
            clear_output()
            display(HTML(f"<h4>Segmented Data Preview (showing {min(20, len(result_df))} of {len(result_df)} rows)</h4>"))
            display(result_df.head(20).style.set_properties(**{'font-size': '10px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f0f0f0'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        seg_status.value = f"<p style='color:green;'>✅ K-Means complete! <b>{k}</b> segments. Name them in Tab 4.</p>"
        apply_names_btn.disabled = False
        names_status.value = "<p>Name your segments and click Apply Names.</p>"

        # Enable traction mapping
        value_check.options = processed_cols
        value_check.value = ()
        value_check.disabled = False
        access_check.options = processed_cols
        access_check.value = ()
        access_check.disabled = False
        evidence_check.options = processed_cols
        evidence_check.value = ()
        evidence_check.disabled = False
        mapping_status.value = "<p>Select variables for each component. Weights auto-populate from selections.</p>"

        tabs.selected_index = 3
    except Exception as e:
        seg_status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"

def handle_apply_names(b):
    global state
    k = state['k_value']
    labels = state['segment_labels']
    df_proc = state['df_processed']
    names_text = segment_names_input.value
    names = parse_segment_names(names_text, k)
    state['segment_names'] = names

    if df_proc is not None and labels is not None:
        result_df = df_proc.copy()
        result_df["Segment"] = [names[l] for l in labels]

        with labeled_output:
            clear_output()
            display(HTML(f"<h4>Segmented Data Preview (showing {min(20, len(result_df))} of {len(result_df)} rows)</h4>"))
            display(result_df.head(20).style.set_properties(**{'font-size': '10px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f0f0f0'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

    names_status.value = f"<p style='color:green;'>✅ Names applied: {', '.join(names)}</p>"

def update_weight_editor(change):
    global state
    processed_cols = state['processed_vars']
    if not processed_cols:
        return
    value_vars = list(value_check.value)
    access_vars = list(access_check.value)
    evidence_vars = list(evidence_check.value)
    weight_editor.value = build_weight_text(value_vars, access_vars, evidence_vars)

def handle_clear_weights(b):
    global state
    weight_editor.value = ''
    value_check.value = ()
    access_check.value = ()
    evidence_check.value = ()

def handle_traction(b):
    global state
    df_proc = state['df_processed']
    labels = state['segment_labels']
    segment_names = state['segment_names']
    weight_text = weight_editor.value
    df_raw = state['df_raw']

    if df_proc is None:
        traction_status.value = "<p style='color:red;'>❌ Run segmentation in Tab 3 first.</p>"
        return

    weights = parse_weights(weight_text)
    if not weights:
        traction_status.value = "<p style='color:red;'>❌ Set weights in Tab 5 first. Check variables and assign weights.</p>"
        return

    value_vars = [v for v, w in weights.items() if w.get("Value", 0) > 0]
    access_vars = [v for v, w in weights.items() if w.get("Access", 0) > 0]
    evidence_vars = [v for v, w in weights.items() if w.get("Evidence", 0) > 0]

    if not value_vars or not access_vars or not evidence_vars:
        traction_status.value = "<p style='color:red;'>❌ Each component needs at least one variable with weight > 0.</p>"
        return

    try:
        analysis_df = df_proc.copy()
        if labels is not None:
            analysis_df["Segment"] = [segment_names[l] for l in labels]
        else:
            analysis_df["Segment"] = "Overall"

        # Min-max normalize only numeric columns (exclude Segment)
        numeric_cols = [c for c in analysis_df.columns if c != "Segment" and pd.api.types.is_numeric_dtype(analysis_df[c])]
        analysis_norm = analysis_df.copy()
        for col in numeric_cols:
            col_min = analysis_df[col].min()
            col_max = analysis_df[col].max()
            if col_max > col_min:
                analysis_norm[col] = (analysis_df[col] - col_min) / (col_max - col_min)
            else:
                analysis_norm[col] = 0.5

        # ── Row-level scoring function ──────────────────────────────
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

        # Apply row-level scoring
        individual_scores = analysis_norm[numeric_cols].apply(score_row, axis=1)

        # Build scored dataframe using ORIGINAL raw data + scores
        scored_df = df_raw.copy() if df_raw is not None else df_proc.copy()
        scored_df["Segment"] = analysis_df["Segment"]
        scored_df["Value_score"] = individual_scores["Value_score"].values
        scored_df["Access_score"] = individual_scores["Access_score"].values
        scored_df["Evidence_score"] = individual_scores["Evidence_score"].values
        scored_df["Traction_quotient"] = individual_scores["Traction_quotient"].values

        # Segment rank (1 = best traction mean)
        seg_traction_mean = scored_df.groupby("Segment")["Traction_quotient"].mean().sort_values(ascending=False)
        seg_rank_map = {seg: i+1 for i, seg in enumerate(seg_traction_mean.index)}
        scored_df["Segment_rank"] = scored_df["Segment"].map(seg_rank_map)

        state['scored_df'] = scored_df

        # ── Overall Sample ──────────────────────────────────────────
        v_ov = scored_df["Value_score"].mean()
        a_ov = scored_df["Access_score"].mean()
        e_ov = scored_df["Evidence_score"].mean()
        traction_ov = scored_df["Traction_quotient"].mean()

        overall_result = pd.DataFrame({
            "Metric": ["Size_Count", "Size_Pct", "Value", "Access", "Evidence", "Traction"],
            "Overall_Sample": [
                len(scored_df), 100.0, round(v_ov, 4), round(a_ov, 4), round(e_ov, 4), round(traction_ov, 4)
            ]
        })

        with overall_output:
            clear_output()
            display(HTML("<h4>Overall Sample Traction (K=1 Baseline)</h4>"))
            display(overall_result.style.set_properties(**{'font-size': '11px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#e8f4f8'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        # ── Segment-wise ────────────────────────────────────────────
        if labels is not None:
            segments = sorted(scored_df["Segment"].unique())
            segment_results = []

            for seg in segments:
                seg_data = scored_df[scored_df["Segment"] == seg]
                v_s = seg_data["Value_score"].mean()
                a_s = seg_data["Access_score"].mean()
                e_s = seg_data["Evidence_score"].mean()
                traction_s = seg_data["Traction_quotient"].mean()
                size_count = len(seg_data)
                size_pct = size_count / len(scored_df) * 100

                segment_results.append({
                    "Segment": seg,
                    "Size_Count": size_count,
                    "Size_Pct": round(size_pct, 4),
                    "Value": round(v_s, 4),
                    "Access": round(a_s, 4),
                    "Evidence": round(e_s, 4),
                    "Traction": round(traction_s, 4)
                })

            seg_df = pd.DataFrame(segment_results)
            seg_df = seg_df.sort_values("Traction", ascending=False)

            transposed = seg_df.set_index("Segment").T
            transposed.index.name = "Metric"
            transposed = transposed.reset_index()

            rankings = []
            for _, row in seg_df.iterrows():
                seg = row["Segment"]
                v, a, e, t = row["Value"], row["Access"], row["Evidence"], row["Traction"]

                if v > 0.6 and a > 0.6 and e > 0.6:
                    name = f"🏆 {seg} (High Traction)"
                elif v > 0.5 and a < 0.3 and e < 0.3:
                    name = f"⚠️ {seg} (High Activity, Low Conversion)"
                elif v < 0.3 and a < 0.3 and e < 0.3:
                    name = f"💤 {seg} (Low Engagement)"
                elif e > 0.5:
                    name = f"💰 {seg} (High Conversion)"
                elif v > 0.5:
                    name = f"🔥 {seg} (High Engagement)"
                else:
                    name = f"❓ {seg} (Mixed Profile)"

                rankings.append(name)
                rankings.append(f"   Value={v:.4f} | Access={a:.4f} | Evidence={e:.4f} | Traction={t:.4f}")
                rankings.append("")

            ranking_text = "\n".join(rankings)
        else:
            transposed = None
            ranking_text = "No segmentation run yet."

        with segment_output:
            clear_output()
            display(HTML("<h4>Segment-wise Traction (Transposed for AI Copy-Paste)</h4>"))
            display(transposed.style.set_properties(**{'font-size': '11px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#e8f4f8'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        ranking_txt.value = ranking_text

        # ── Individual scores preview ─────────────────────────────
        preview_cols = ["Segment", "Value_score", "Access_score", "Evidence_score", "Traction_quotient", "Segment_rank"]
        if df_raw is not None and len(df_raw.columns) > 0:
            id_col = df_raw.columns[0]
            if id_col in scored_df.columns:
                preview_cols = [id_col] + preview_cols

        individual_preview = scored_df[preview_cols].head(10)

        with individual_output:
            clear_output()
            display(HTML(f"<h4>Individual Scores Preview (first 10 of {len(scored_df)} rows)</h4>"))
            display(individual_preview.style.set_properties(**{'font-size': '10px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f0f0f0'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        # ── Histogram ───────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(10, 6))
        segments_ordered = seg_df["Segment"].tolist() if labels is not None else ["Overall"]
        colors = plt.cm.Set2(np.linspace(0, 1, len(segments_ordered)))

        for i, seg in enumerate(segments_ordered):
            seg_data = scored_df[scored_df["Segment"] == seg]["Traction_quotient"]
            ax.hist(seg_data, bins=30, alpha=0.6, label=seg, color=colors[i], edgecolor='white')

        ax.axvline(scored_df["Traction_quotient"].mean(), color='black', linestyle='--', linewidth=2, 
                   label=f'Overall Mean={scored_df["Traction_quotient"].mean():.4f}')
        ax.set_xlabel("Traction Quotient", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.set_title("Distribution of Individual Traction Scores by Segment", fontsize=14, fontweight='bold')
        ax.legend(title="Segments", loc='best')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        with traction_hist_output:
            clear_output()
            display(fig)
        plt.close(fig)

        traction_status.value = f"<p style='color:green;'>✅ Traction computed for <b>{len(scored_df):,}</b> individuals. Overall mean={scored_df['Traction_quotient'].mean():.4f}</p>"
        export_report_btn.disabled = False
        export_csv_btn.disabled = False
        export_status.value = "<p>Click Download to export the report or scored data.</p>"

        tabs.selected_index = 5

    except Exception as e:
        traction_status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"

def handle_export_report(b):
    global state
    df_proc = state['df_processed']
    labels = state['segment_labels']
    segment_names = state['segment_names']
    weight_text = weight_editor.value
    reflection = reflection_box.value
    scored_df = state['scored_df']

    if df_proc is None:
        export_status.value = "<p style='color:red;'>❌ Run full analysis before exporting.</p>"
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_lines = [
        "# Customer Segmentation & Traction Audit Report",
        "",
        f"**Generated:** {timestamp}",
        f"**Dataset:** {len(df_proc):,} rows × {len(df_proc.columns)} columns",
        "",
        "---",
        "",
        "## 1. Segment Names",
        ""
    ]
    for i, name in enumerate(segment_names):
        report_lines.append(f"- {name}")

    report_lines.extend([
        "",
        "---",
        "",
        "## 2. Reflection",
        "",
        reflection if reflection else "*(No reflection provided)*",
        "",
        "---",
        "",
        "## 3. Variable Weights",
        "",
        "```",
        weight_text if weight_text else "(No weights set)",
        "```",
        "",
        "---",
        "",
        "## 4. Traction Results",
        "",
        f"**Overall Mean Traction:** {scored_df['Traction_quotient'].mean():.4f}" if scored_df is not None else "",
        "",
        "### Individual Scores Summary",
        ""
    ])

    if scored_df is not None:
        report_lines.append(f"- Total individuals: {len(scored_df):,}")
        report_lines.append(f"- Mean Value: {scored_df['Value_score'].mean():.4f}")
        report_lines.append(f"- Mean Access: {scored_df['Access_score'].mean():.4f}")
        report_lines.append(f"- Mean Evidence: {scored_df['Evidence_score'].mean():.4f}")
        report_lines.append(f"- Mean Traction: {scored_df['Traction_quotient'].mean():.4f}")

    report_lines.extend([
        "",
        "---",
        "",
        "*End of Report*"
    ])

    report_text = "\n".join(report_lines)
    report_path = "/tmp/traction_report.txt"
    with open(report_path, "w") as f:
        f.write(report_text)

    export_status.value = f"""
    <div style="background:#d4edda; padding:10px; border-radius:6px; border-left:4px solid #28a745;">
        <b>✅ Report saved</b><br>
        Path: {report_path}<br><br>
        <b>To download:</b> Copy the path above and run in a new cell:<br>
        <code>from google.colab import files; files.download('{report_path}')</code>
    </div>
    """

def handle_export_csv(b):
    global state
    scored_df = state['scored_df']

    if scored_df is None:
        export_status.value = "<p style='color:red;'>❌ Calculate traction first before exporting CSV.</p>"
        return

    csv_path = "/tmp/scored_data.csv"
    scored_df.to_csv(csv_path, index=False)

    export_status.value = f"""
    <div style="background:#d4edda; padding:10px; border-radius:6px; border-left:4px solid #28a745;">
        <b>✅ Report saved</b><br>
        Path: {report_path}<br><br>
        <b>To download:</b> Copy the path above and run in a new cell:<br>
        <code>from google.colab import files; files.download('{report_path}')</code>
    </div>
    """

# ── Wire up events ────────────────────────────────────────────────────
file_in.observe(handle_upload, names='value')
basis_check.observe(handle_basis_change, names='value')
cat_check.observe(handle_cat_change, names='value')
confirm_btn.on_click(handle_confirm)
run_btn.on_click(handle_run)
apply_names_btn.on_click(handle_apply_names)
value_check.observe(update_weight_editor, names='value')
access_check.observe(update_weight_editor, names='value')
evidence_check.observe(update_weight_editor, names='value')
clear_weights_btn.on_click(handle_clear_weights)
calc_btn.on_click(handle_traction)
export_report_btn.on_click(handle_export_report)
export_csv_btn.on_click(handle_export_csv)

# ── Display ───────────────────────────────────────────────────────────
display(widgets.HTML("<h1>🎯 Customer Segmentation & Traction Audit</h1>"))
display(widgets.HTML("<p><b>Upload any dataset, segment via K-Means, map to Traction Equation, score individuals, and export results.</b></p>"))
display(tabs)
