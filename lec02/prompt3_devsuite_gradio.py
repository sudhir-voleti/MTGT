# ═══════════════════════════════════════════════════════════════════════
# Caselet 1: 4-Tab Gradio App — FIXED: Standardize before K-Means, 3-decimal centroids
# Paste into ONE Colab cell and run
# ═══════════════════════════════════════════════════════════════════════

# ── Quiet install ─────────────────────────────────────────────────────
import subprocess, sys
for pkg in ["gradio", "scikit-learn", "pandas", "matplotlib", "seaborn"]:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg])

# ── Imports ─────────────────────────────────────────────────────────────
import gradio as gr
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── Build app ───────────────────────────────────────────────────────────

with gr.Blocks(title="Caselet 1: Customer Segmentation", theme=gr.themes.Soft()) as app:

    gr.Markdown("""
    # 🎯 Caselet 1: Customer Segmentation
    **Upload data, select variables, run K-Means clustering, and explore results.**
    """)

    # ── States ──────────────────────────────────────────────────────────
    df_raw = gr.State(None)
    df_processed = gr.State(None)
    processed_vars = gr.State([])
    X_scaled_state = gr.State(None)  # store scaled data for K-Means

    # ═════════════════════════════════════════════════════════════════
    # TAB 1: Data Preview
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
                gr.Markdown("### Raw Data Preview")
                html_preview = gr.HTML(
                    value="<p style='color:#888;'>Upload a CSV to see data preview.</p>"
                )

        gr.Markdown("### Dataset Overview")
        desc_stats = gr.Textbox(
            label="Descriptive Statistics",
            value="Upload a CSV to see dataset summary.",
            lines=10,
            interactive=False
        )

    # ═════════════════════════════════════════════════════════════════
    # TAB 2: Variable Selection
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("🔧 Variable Selection"):

        gr.Markdown("## Configure Variables for Clustering")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Step A: Select Basis Variables")
                gr.Markdown("Check all variables to include in the analysis.")
                basis_check = gr.CheckboxGroup(
                    choices=["(Upload CSV first)"],
                    label="Available Variables",
                    interactive=False
                )

            with gr.Column(scale=1):
                gr.Markdown("### Step B: Mark Categorical Variables")
                gr.Markdown("From selected basis variables, check those needing dummy encoding.")
                cat_check = gr.CheckboxGroup(
                    choices=["(Select basis variables first)"],
                    label="Categorical Variables (Dummy Encoding)",
                    interactive=False
                )

        gr.Markdown("---")
        gr.Markdown("### Variable Summary")
        summary = gr.Textbox(
            label="Selection Summary",
            value="Upload CSV and select variables to see summary.",
            lines=12,
            interactive=False
        )

        confirm_btn = gr.Button("✅ Confirm Selection & Create Dummies", variant="primary", size="lg")
        confirm_status = gr.Textbox(
            label="Processing Status",
            value="Select variables and click Confirm to prepare data.",
            interactive=False
        )

    # ═════════════════════════════════════════════════════════════════
    # TAB 3: Segmentation
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("🎯 Segmentation"):

        gr.Markdown("## K-Means Clustering")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Step 1: Review Scree Plot")
                gr.Markdown("The elbow suggests optimal K. Pick a value and run.")
                scree_img = gr.Image(
                    label="Scree Plot (Elbow Method)",
                    type="filepath",
                    interactive=False
                )

                gr.Markdown("### Step 2: Choose K")
                k_slider = gr.Slider(
                    minimum=2, maximum=10, step=1, value=3,
                    label="Number of Segments (K)"
                )

                run_btn = gr.Button("▶️ Run Segmentation", variant="primary", size="lg")
                seg_status = gr.Textbox(
                    label="Segmentation Status",
                    value="Confirm variables in Tab 2 first.",
                    interactive=False
                )

            with gr.Column(scale=2):
                gr.Markdown("### WCSS Values")
                wcss_table = gr.Dataframe(
                    label="Within-Cluster Sum of Squares by K",
                    interactive=False
                )

    # ═════════════════════════════════════════════════════════════════
    # TAB 4: Results
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("📊 Results"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Segment Sizes")
                sizes_tbl = gr.Dataframe(
                    label="Count & Percentage",
                    interactive=False
                )

            with gr.Column(scale=2):
                gr.Markdown("### Centroids (Standardized Scale, 3 decimals)")
                cents_tbl = gr.Dataframe(
                    label="Cluster Centroids",
                    interactive=False
                )

        gr.Markdown("---")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### PCA Scatter Plot")
                scatter_img = gr.Image(
                    label="Segment Visualization",
                    type="filepath",
                    interactive=False
                )

            with gr.Column(scale=2):
                gr.Markdown("### Segmented Data Preview")
                labeled_tbl = gr.Dataframe(
                    label="Data with Segment Labels",
                    interactive=False,
                    wrap=True
                )

    # ═════════════════════════════════════════════════════════════════
    # CALLBACKS
    # ═════════════════════════════════════════════════════════════════

    def handle_upload(fp):
        if fp is None:
            return (
                None,
                "<p style='color:#888;'>Upload a CSV to see data preview.</p>",
                gr.CheckboxGroup(choices=["(Upload CSV first)"], value=[], interactive=False),
                gr.CheckboxGroup(choices=["(Select basis variables first)"], value=[], interactive=False),
                "Waiting for CSV upload...",
                "Upload a CSV to see dataset summary.",
                "Select variables and click Confirm to prepare data.",
                None, None, None, None
            )

        try:
            df = pd.read_csv(fp)
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

            return (
                df,
                styled_html,
                gr.CheckboxGroup(choices=all_cols, value=[], interactive=True),
                gr.CheckboxGroup(choices=["(Select basis variables first)"], value=[], interactive=False),
                f"✅ Loaded: {len(df):,} rows × {len(df.columns)} columns",
                "\n".join(stats_lines),
                "Select variables and click Confirm to prepare data.",
                None, None, None, None
            )

        except Exception as e:
            return (
                None,
                f"<p style='color:red;'>Error: {str(e)}</p>",
                gr.CheckboxGroup(choices=["(Error)"], value=[], interactive=False),
                gr.CheckboxGroup(choices=["(Error)"], value=[], interactive=False),
                f"❌ Error: {str(e)}",
                f"Error: {str(e)}",
                "Error loading file.",
                None, None, None, None
            )

    def handle_basis_change(df, selected_basis):
        if df is None or not selected_basis:
            return (
                gr.CheckboxGroup(choices=["(Select basis variables first)"], value=[], interactive=False),
                "Upload CSV and select basis variables."
            )

        cat_choices = selected_basis if selected_basis else ["(Select basis variables first)"]

        lines = [f"📊 Basis variables: {len(selected_basis)}"]
        for v in selected_basis:
            dtype = str(df[v].dtype)
            n_unique = df[v].nunique()
            lines.append(f"  • {v}: {dtype} | {n_unique} unique")

        return (
            gr.CheckboxGroup(choices=cat_choices, value=[], interactive=True),
            "\n".join(lines)
        )

    def handle_cat_change(df, selected_basis, selected_cat):
        if df is None or not selected_basis:
            return "Upload CSV and select basis variables."

        selected_cat = selected_cat or []
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
            dtype = str(df[v].dtype)
            lines.append(f"  {marker} {v} ({dtype})")

        if selected_cat:
            lines.append("")
            lines.append("Dummy variables to create (n-1, first category as base):")
            for v in selected_cat:
                n_cats = df[v].nunique()
                lines.append(f"  • {v}: {n_cats} categories → {n_cats - 1} dummies")

        return "\n".join(lines)

    # ── Tab 2: Confirm & create dummies + standardize ─────────────────
    def handle_confirm(df, selected_basis, selected_cat):
        if df is None or not selected_basis:
            return None, [], None, "❌ Please select basis variables first.", None, None

        selected_cat = selected_cat or []

        # Build processed dataframe
        df_proc = df[selected_basis].copy()
        df_proc = df_proc.dropna()
        if len(df_proc) < 2:
            return None, [], None, "❌ Not enough valid rows after dropping missing values.", None, None

        # Create (n-1) dummies for categorical vars
        for col in selected_cat:
            if col in df_proc.columns:
                dummies = pd.get_dummies(df_proc[col], prefix=col, drop_first=True)
                dummies = dummies.astype(int)
                df_proc = pd.concat([df_proc.drop(columns=[col]), dummies], axis=1)

        # Ensure all numeric
        non_numeric = df_proc.select_dtypes(exclude=[np.number]).columns.tolist()
        if non_numeric:
            return None, [], None, f"❌ Non-numeric columns remain: {non_numeric}", None, None

        final_cols = df_proc.columns.tolist()

        # Standardize ONCE here, store for K-Means
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_proc.values)

        # Compute scree plot on standardized data
        wcss = []
        ks = range(1, min(11, len(X_scaled)))
        for k in ks:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            wcss.append(km.inertia_)

        # Enhanced scree plot with elbow annotation and % drop
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(list(ks), wcss, 'bo-', linewidth=2.5, markersize=9, color='#2E86AB')

        # Annotate % drop between consecutive K values
        for i in range(1, len(wcss)):
            pct_drop = (wcss[i-1] - wcss[i]) / wcss[i-1] * 100
            ax.annotate(
                f"{pct_drop:.1f}%",
                xy=(i+1, wcss[i]),
                xytext=(5, 10),
                textcoords='offset points',
                fontsize=8,
                color='#555',
                alpha=0.8
            )

        # Highlight suggested elbow (largest % drop)
        if len(wcss) > 2:
            drops = [(wcss[i-1] - wcss[i]) / wcss[i-1] * 100 for i in range(1, len(wcss))]
            best_k = drops.index(max(drops)) + 2  # +2 because drops start at K=2
            ax.axvline(x=best_k, color='red', linestyle='--', alpha=0.5, label=f'Suggested K={best_k}')
            ax.legend()

        ax.set_xlabel('K (Number of Segments)', fontsize=12)
        ax.set_ylabel('WCSS (Standardized Data)', fontsize=12)
        ax.set_title('Scree Plot with % Drop Annotations', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(list(ks))

        plt.tight_layout()
        scree_path = "/tmp/scree_plot.png"
        plt.savefig(scree_path, dpi=150, bbox_inches='tight')
        plt.close(fig)

        # WCSS table
        wcss_df = pd.DataFrame({"K": list(ks), "WCSS": [round(w, 2) for w in wcss]})
        # Add % drop column
        pct_drops = [None] + [round((wcss[i-1] - wcss[i]) / wcss[i-1] * 100, 1) for i in range(1, len(wcss))]
        wcss_df["Pct_Drop"] = pct_drops

        return (
            df_proc,
            final_cols,
            X_scaled,
            f"✅ Standardized & dummies ready! {len(df_proc):,} rows × {len(final_cols)} columns.",
            scree_path,
            wcss_df
        )

    # ── Tab 3: Run segmentation on PRE-STANDARDIZED data ────────────
    def handle_run(df_proc, processed_cols, X_scaled, k):
        if df_proc is None or X_scaled is None:
            return None, None, None, None, "❌ Confirm variables in Tab 2 first."

        if len(X_scaled) < k:
            return None, None, None, None, f"❌ Need ≥{k} rows for K={k}."

        # K-Means on ALREADY standardized data
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)

        # Centroids are ALREADY in standardized space — just round to 3 decimals
        cents = pd.DataFrame(
            np.round(km.cluster_centers_, 3),
            columns=processed_cols,
            index=[f"Segment {i+1}" for i in range(k)]
        )

        # Segment sizes
        sizes = pd.Series(labels).value_counts().sort_index()
        sizes_df = pd.DataFrame({
            "Segment": [f"Segment {i+1}" for i in sizes.index],
            "Count": sizes.values,
            "Pct": (sizes.values / len(labels) * 100).round(1)
        })

        # PCA scatter on standardized data
        pca = PCA(n_components=2)
        Xp = pca.fit_transform(X_scaled)

        fig, ax = plt.subplots(figsize=(9, 6))
        colors = plt.cm.Set2(np.linspace(0, 1, k))
        for i in range(k):
            mask = labels == i
            ax.scatter(Xp[mask, 0], Xp[mask, 1], c=[colors[i]],
                       label=f"Seg {i+1}", alpha=0.7, s=80,
                       edgecolors='white', linewidth=0.5)
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})", fontsize=11)
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})", fontsize=11)
        ax.set_title("Segment Scatter Plot (PCA of Standardized Data)", fontsize=14, fontweight='bold')
        ax.legend(title="Segments", loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        scatter_path = "/tmp/scatter_plot.png"
        plt.savefig(scatter_path, dpi=150, bbox_inches='tight')
        plt.close(fig)

        # Labeled data preview
        result_df = df_proc.copy()
        result_df["Segment"] = [f"Segment {l+1}" for l in labels]

        return (
            cents,
            sizes_df,
            scatter_path,
            result_df.head(20),
            f"✅ K-Means complete! {k} segments on {len(df_proc):,} standardized observations."
        )

    # ═════════════════════════════════════════════════════════════════
    # WIRE UP
    # ═════════════════════════════════════════════════════════════════

    file_in.change(
        fn=handle_upload,
        inputs=file_in,
        outputs=[df_raw, html_preview, basis_check, cat_check, status, desc_stats, confirm_status, df_processed, processed_vars, X_scaled_state, scree_img]
    )

    basis_check.change(
        fn=handle_basis_change,
        inputs=[df_raw, basis_check],
        outputs=[cat_check, summary]
    )

    cat_check.change(
        fn=handle_cat_change,
        inputs=[df_raw, basis_check, cat_check],
        outputs=summary
    )

    confirm_btn.click(
        fn=handle_confirm,
        inputs=[df_raw, basis_check, cat_check],
        outputs=[df_processed, processed_vars, X_scaled_state, confirm_status, scree_img, wcss_table]
    )

    run_btn.click(
        fn=handle_run,
        inputs=[df_processed, processed_vars, X_scaled_state, k_slider],
        outputs=[cents_tbl, sizes_tbl, scatter_img, labeled_tbl, seg_status]
    )

# ── Launch ──────────────────────────────────────────────────────────────
app.launch(share=True, debug=True)
