# ═══════════════════════════════════════════════════════════════════════
# Caselet 1: Step 1 — Data Preview + Variable Selection (ipywidgets)
# Paste into ONE Jupyter/Colab cell and run
# ═══════════════════════════════════════════════════════════════════════

# ── Quiet install ─────────────────────────────────────────────────────
import subprocess, sys
for pkg in ["ipywidgets", "pandas", "numpy"]:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg])

# ── Imports ─────────────────────────────────────────────────────────────
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import pandas as pd
import numpy as np
import io

# ── Global State ────────────────────────────────────────────────────────
df_state = None  # Replaces gr.State(None)

# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: DATA PREVIEW
# ═══════════════════════════════════════════════════════════════════════

# File upload (replaces gr.File)
file_in = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='📁 Upload CSV',
    layout=widgets.Layout(width='200px')
)

status = widgets.HTML(value="<p style='color:#888;'>Waiting for CSV upload...</p>")

# HTML preview area (replaces gr.HTML)
# Using Output widget for dynamic table display
preview_output = widgets.Output()
with preview_output:
    display(HTML("<p style='color:#888;'>Upload a CSV to see data preview.</p>"))

# Descriptive stats (replaces gr.Textbox)
desc_stats = widgets.Textarea(
    value="Upload a CSV to see dataset summary.",
    description='Overview:',
    layout=widgets.Layout(width='100%', height='250px'),
    disabled=True
)

data_preview_section = widgets.VBox([
    widgets.HTML("<h2>📁 Data Preview</h2>"),
    widgets.HBox([file_in, status]),
    widgets.HTML("<h4>Raw Data Preview</h4>"),
    preview_output,
    widgets.HTML("<h4>Dataset Overview</h4>"),
    desc_stats
])

# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: VARIABLE SELECTION
# ═══════════════════════════════════════════════════════════════════════

# Basis variable checklist (replaces gr.CheckboxGroup)
# Using SelectMultiple for multi-select (closest to CheckboxGroup)
basis_check = widgets.SelectMultiple(
    options=['(Upload CSV first)'],
    value=(),
    description='Basis vars:',
    rows=8,
    layout=widgets.Layout(width='350px'),
    disabled=True
)

# Categorical variable checklist (replaces gr.CheckboxGroup)
cat_check = widgets.SelectMultiple(
    options=['(Select basis variables first)'],
    value=(),
    description='Categorical:',
    rows=8,
    layout=widgets.Layout(width='350px'),
    disabled=True
)

# Summary (replaces gr.Textbox)
summary = widgets.Textarea(
    value="Upload CSV and select variables to see summary.",
    description='Summary:',
    layout=widgets.Layout(width='100%', height='300px'),
    disabled=True
)

variable_selection_section = widgets.VBox([
    widgets.HTML("<h2>🔧 Variable Selection</h2>"),
    widgets.HTML("<h3>Configure Variables for Clustering</h3>"),
    widgets.HTML("<p><b>Step A:</b> Select basis variables to include in the analysis.</p>"),
    widgets.HBox([basis_check, widgets.VBox([
        widgets.HTML("<p><b>Step B:</b> From selected basis variables, check those needing dummy encoding.</p>"),
        cat_check
    ])]),
    widgets.HTML("<h4>Variable Summary</h4>"),
    summary
])

# ═══════════════════════════════════════════════════════════════════════
# ASSEMBLE TABS
# ═══════════════════════════════════════════════════════════════════════

tabs = widgets.Tab(children=[data_preview_section, variable_selection_section])
tabs.set_title(0, '📁 Data Preview')
tabs.set_title(1, '🔧 Variable Selection')

# ═══════════════════════════════════════════════════════════════════════
# CALLBACKS
# ═══════════════════════════════════════════════════════════════════════

def handle_upload(change):
    """CSV upload: load data, populate HTML preview, desc stats, and basis checklist."""
    global df_state

    if not file_in.value:
        return

    try:
        # Get uploaded file content
        uploaded = list(file_in.value.values())[0]
        content = uploaded['content']
        df = pd.read_csv(io.BytesIO(content))
        df_state = df
        all_cols = df.columns.tolist()

        # HTML preview with horizontal scroll — styled like Jupyter
        html = df.head(10).to_html(
            index=False,
            classes='table table-striped',
            border=0,
            max_rows=10
        )
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

        # Build descriptive stats
        stats_lines = [
            f"📊 Rows: {len(df):,}",
            f"📊 Columns: {len(df.columns)}",
            f"📊 Numeric columns: {len(df.select_dtypes(include=[np.number]).columns)}",
            f"📊 Categorical/object columns: {len(df.select_dtypes(include=['object', 'category']).columns)}",
            f"📊 Missing values: {df.isnull().sum().sum():,} ({100*df.isnull().sum().sum()/(df.shape[0]*df.shape[1]):.1f}%)",
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

        # Update basis checklist
        basis_check.options = all_cols
        basis_check.value = ()
        basis_check.disabled = False

        # Reset categorical
        cat_check.options = ['(Select basis variables first)']
        cat_check.value = ()
        cat_check.disabled = True

        summary.value = "Upload CSV and select basis variables."

    except Exception as e:
        status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"
        with preview_output:
            clear_output()
            display(HTML(f"<p style='color:red;'>Error: {str(e)}</p>"))

def handle_basis_change(change):
    """Update categorical options and summary when basis variables change."""
    global df_state

    if df_state is None:
        return

    selected_basis = list(basis_check.value)

    if not selected_basis:
        cat_check.options = ['(Select basis variables first)']
        cat_check.value = ()
        cat_check.disabled = True
        summary.value = "Upload CSV and select basis variables."
        return

    # Update categorical options from selected basis
    cat_check.options = selected_basis
    cat_check.value = ()
    cat_check.disabled = False

    # Update summary
    lines = [f"📊 Basis variables selected: {len(selected_basis)}"]
    for v in selected_basis:
        dtype = str(df_state[v].dtype)
        n_unique = df_state[v].nunique()
        lines.append(f"  • {v}: {dtype} | {n_unique} unique values")

    summary.value = "\n".join(lines)

def handle_cat_change(change):
    """Update summary when categorical variables are selected."""
    global df_state

    if df_state is None:
        return

    selected_basis = list(basis_check.value)
    selected_cat = list(cat_check.value)

    if not selected_basis:
        summary.value = "Upload CSV and select basis variables."
        return

    numeric_vars = [v for v in selected_basis if v not in selected_cat]

    lines = [
        f"📊 Total basis variables: {len(selected_basis)}",
        f"🔤 Categorical (dummy encoding): {len(selected_cat)}",
        f"🔢 Numeric (direct use): {len(numeric_vars)}",
        "",
        "Final variable list for clustering:"
    ]
    for v in selected_basis:
        marker = "🔤" if v in selected_cat else "🔢"
        dtype = str(df_state[v].dtype)
        lines.append(f"  {marker} {v}  ({dtype})")

    if selected_cat:
        lines.append("")
        lines.append("Dummy variables will be created for:")
        for v in selected_cat:
            n_cats = df_state[v].nunique()
            lines.append(f"  • {v}: {n_cats} categories → {n_cats} dummies")

    summary.value = "\n".join(lines)

# Wire up events (replaces Gradio .change() callbacks)
file_in.observe(handle_upload, names='value')
basis_check.observe(handle_basis_change, names='value')
cat_check.observe(handle_cat_change, names='value')

# ── Display ─────────────────────────────────────────────────────────────
display(widgets.HTML("<h1>🎯 Caselet 1: Customer Segmentation</h1>"))
display(widgets.HTML("<p><b>Step 1 — Upload data and configure variables for clustering.</b></p>"))
display(tabs)
