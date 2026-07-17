# ═══════════════════════════════════════════════════════════════════════
# Caselet 1: Step 1 — Data Preview (HTML) + Variable Selection (Checkbox)
# Paste into ONE Colab cell and run
# ═══════════════════════════════════════════════════════════════════════

# ── Quiet install ─────────────────────────────────────────────────────
import subprocess, sys
for pkg in ["gradio", "pandas", "numpy"]:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg])

# ── Imports ─────────────────────────────────────────────────────────────
import gradio as gr
import pandas as pd
import numpy as np

# ── Build app ───────────────────────────────────────────────────────────

with gr.Blocks(title="Caselet 1: Customer Segmentation", theme=gr.themes.Soft()) as app:

    gr.Markdown("""
    # 🎯 Caselet 1: Customer Segmentation
    **Step 1 — Upload data and configure variables for clustering.**
    """)

    df_state = gr.State(None)

    # ═════════════════════════════════════════════════════════════════
    # TAB 1: Data Preview (HTML table like Colab/Jupyter)
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("📁 Data Preview"):
        with gr.Row():
            with gr.Column(scale=1):
                file_in = gr.File(
                    label="Upload CSV File",
                    file_types=[".csv"],
                    type="filepath"
                )
                status = gr.Textbox(
                    label="Status",
                    value="Waiting for CSV upload...",
                    interactive=False
                )

            with gr.Column(scale=2):
                # HTML preview with horizontal scroll — mimics Colab pandas
                gr.Markdown("### Raw Data Preview")
                html_preview = gr.HTML(
                    value="<p style='color:#888;'>Upload a CSV to see data preview.</p>"
                )

        # Basic descriptive stats below
        gr.Markdown("### Dataset Overview")
        desc_stats = gr.Textbox(
            label="Descriptive Statistics",
            value="Upload a CSV to see dataset summary.",
            lines=10,
            interactive=False
        )

    # ═════════════════════════════════════════════════════════════════
    # TAB 2: Variable Selection (Checkbox groups)
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("🔧 Variable Selection"):

        gr.Markdown("## Configure Variables for Clustering")

        with gr.Row():
            # Left: Basis variable checklist
            with gr.Column(scale=1):
                gr.Markdown("### Step A: Select Basis Variables")
                gr.Markdown("Check all variables to include in the analysis.")
                basis_check = gr.CheckboxGroup(
                    choices=["(Upload CSV first)"],
                    label="Available Variables",
                    interactive=False
                )

            # Right: Categorical subset
            with gr.Column(scale=1):
                gr.Markdown("### Step B: Mark Categorical Variables")
                gr.Markdown("From selected basis variables, check those needing dummy encoding.")
                cat_check = gr.CheckboxGroup(
                    choices=["(Select basis variables first)"],
                    label="Categorical Variables (Dummy Encoding)",
                    interactive=False
                )

        # Summary panel
        gr.Markdown("---")
        gr.Markdown("### Variable Summary")
        summary = gr.Textbox(
            label="Selection Summary",
            value="Upload CSV and select variables to see summary.",
            lines=12,
            interactive=False
        )

    # ═════════════════════════════════════════════════════════════════
    # CALLBACKS
    # ═════════════════════════════════════════════════════════════════

    def handle_upload(fp):
        """CSV upload: load data, populate HTML preview, desc stats, and basis checklist."""
        if fp is None:
            return (
                None,
                "<p style='color:#888;'>Upload a CSV to see data preview.</p>",
                gr.CheckboxGroup(choices=["(Upload CSV first)"], value=[], interactive=False),
                gr.CheckboxGroup(choices=["(Select basis variables first)"], value=[], interactive=False),
                "Waiting for CSV upload...",
                "Upload a CSV to see dataset summary."
            )

        try:
            df = pd.read_csv(fp)
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

            desc = "\n".join(stats_lines)

            return (
                df,
                styled_html,
                gr.CheckboxGroup(choices=all_cols, value=[], interactive=True),
                gr.CheckboxGroup(choices=["(Select basis variables first)"], value=[], interactive=False),
                f"✅ Loaded: {len(df):,} rows × {len(df.columns)} columns",
                desc
            )

        except Exception as e:
            return (
                None,
                f"<p style='color:red;'>Error: {str(e)}</p>",
                gr.CheckboxGroup(choices=["(Error loading file)"], value=[], interactive=False),
                gr.CheckboxGroup(choices=["(Error)"], value=[], interactive=False),
                f"❌ Error: {str(e)}",
                f"Error: {str(e)}"
            )

    def handle_basis_change(df, selected_basis):
        """Update categorical options and summary when basis variables change."""
        if df is None or not selected_basis:
            return (
                gr.CheckboxGroup(choices=["(Select basis variables first)"], value=[], interactive=False),
                "Upload CSV and select basis variables."
            )

        cat_choices = selected_basis if selected_basis else ["(Select basis variables first)"]

        lines = [f"📊 Basis variables selected: {len(selected_basis)}"]
        for v in selected_basis:
            dtype = str(df[v].dtype)
            n_unique = df[v].nunique()
            lines.append(f"  • {v}: {dtype} | {n_unique} unique values")

        return (
            gr.CheckboxGroup(choices=cat_choices, value=[], interactive=True),
            "\n".join(lines)
        )

    def handle_cat_change(df, selected_basis, selected_cat):
        """Update summary when categorical variables are selected."""
        if df is None or not selected_basis:
            return "Upload CSV and select basis variables."

        selected_cat = selected_cat or []
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
            dtype = str(df[v].dtype)
            lines.append(f"  {marker} {v}  ({dtype})")

        if selected_cat:
            lines.append("")
            lines.append("Dummy variables will be created for:")
            for v in selected_cat:
                n_cats = df[v].nunique()
                lines.append(f"  • {v}: {n_cats} categories → {n_cats} dummies")

        return "\n".join(lines)

    # Wire up
    file_in.change(
        fn=handle_upload,
        inputs=file_in,
        outputs=[df_state, html_preview, basis_check, cat_check, status, desc_stats]
    )

    basis_check.change(
        fn=handle_basis_change,
        inputs=[df_state, basis_check],
        outputs=[cat_check, summary]
    )

    cat_check.change(
        fn=handle_cat_change,
        inputs=[df_state, basis_check, cat_check],
        outputs=summary
    )

# ── Launch ──────────────────────────────────────────────────────────────
app.launch(share=True, debug=True)
