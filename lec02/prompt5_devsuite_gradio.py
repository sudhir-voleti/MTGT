# ═══════════════════════════════════════════════════════════════════════
# Generic Customer Segmentation & Traction Audit — 6-Tab Gradio App
# FIXED: Individual scoring + reflection moved to Tab 5
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
from datetime import datetime

# ── Build app ───────────────────────────────────────────────────────────

with gr.Blocks(title="Caselet: Customer Segmentation & Traction Audit", theme=gr.themes.Soft()) as app:
    
    gr.Markdown("""
    # 🎯 Customer Segmentation & Traction Audit
    **Upload any dataset, segment via K-Means, map to Traction Equation, score individuals, and export results.**
    """)
    
    # ── States ──────────────────────────────────────────────────────────
    df_raw = gr.State(None)
    df_processed = gr.State(None)
    processed_vars = gr.State([])
    X_scaled_state = gr.State(None)
    segment_labels_state = gr.State(None)
    segment_names_state = gr.State(["Segment 1", "Segment 2", "Segment 3"])
    scored_df_state = gr.State(None)
    
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
    # TAB 4: Results + Segment Naming
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("📊 Results"):
        
        gr.Markdown("## Segmentation Results")
        
        gr.Markdown("---")
        gr.Markdown("### Name Your Segments")
        gr.Markdown("*Enter custom names below (comma-separated, in order). Default: Segment 1, Segment 2, ...*")
        
        segment_names_input = gr.Textbox(
            label="Segment Names",
            value="Segment 1, Segment 2, Segment 3",
            interactive=True
        )
        apply_names_btn = gr.Button("✏️ Apply Names", size="sm")
        names_status = gr.Textbox(
            label="Names Status",
            value="Run segmentation first, then name your segments.",
            interactive=False
        )
        
        gr.Markdown("---")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Segment Sizes")
                sizes_tbl = gr.Dataframe(
                    label="Count & Percentage",
                    interactive=False
                )
            
            with gr.Column(scale=2):
                gr.Markdown("### Centroids (Standardized Scale, 3 decimals)")
                gr.Markdown("*Transposed: Variables as rows, Segments as columns*")
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
    # TAB 5: Mapping Traction Components + Reflection
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("🔧 Mapping Traction Components"):
        
        gr.Markdown("""
        ## Map Variables to Traction Components
        **Step 1:** Check variables for each component. 
        **Step 2:** Reflect on your mapping choices.
        **Step 3:** Set weights (0–1+).
        """)
        
        # ── Step 1: Checkboxes ──────────────────────────────────────
        gr.Markdown("### Step 1: Select Variables per Component")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("**Value** (utility, stickiness, usage)")
                value_check = gr.CheckboxGroup(
                    choices=["(Run segmentation first)"],
                    label="Value Variables",
                    interactive=False
                )
            
            with gr.Column(scale=1):
                gr.Markdown("**Access** (channel efficiency, reach)")
                access_check = gr.CheckboxGroup(
                    choices=["(Run segmentation first)"],
                    label="Access Variables",
                    interactive=False
                )
            
            with gr.Column(scale=1):
                gr.Markdown("**Evidence** (behavioral velocity, conversion)")
                evidence_check = gr.CheckboxGroup(
                    choices=["(Run segmentation first)"],
                    label="Evidence Variables",
                    interactive=False
                )
        
        # ── Step 2: Reflection ──────────────────────────────────────
        gr.Markdown("---")
        gr.Markdown("### Step 2: 📝 Reflect on Your Mapping")
        gr.Markdown("*Why did you map these specific variables to Value/Access/Evidence? What trade-offs did you consider?*")
        
        reflection_box = gr.Textbox(
            label="Your Reflection",
            value="",
            lines=6,
            interactive=True
        )
        
        # ── Step 3: Weight editor ─────────────────────────────────────
        gr.Markdown("---")
        gr.Markdown("### Step 3: Set Weights for Selected Variables")
        gr.Markdown("*Format: `variable_name=Component:weight` one per line. Auto-populates from selections above with default weight=1.*")
        
        weight_editor = gr.Textbox(
            label="Weights (var=Component:weight, one per line)",
            value="",
            lines=10,
            interactive=True
        )
        
        with gr.Row():
            clear_weights_btn = gr.Button("🔄 Clear All", size="sm")
        
        mapping_status = gr.Textbox(
            label="Mapping Status",
            value="Run segmentation first, then select variables and set weights.",
            interactive=False
        )
    
    # ═════════════════════════════════════════════════════════════════
    # TAB 6: Traction Calculation + Individual Scoring + Export
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("📊 Traction Calculation"):
        
        gr.Markdown("""
        ## Traction Results
        **Overall Sample** (K=1, no clustering) vs **Segment-wise** (your named segments)
        """)
        
        calc_btn = gr.Button("📊 Calculate Traction Quotient", variant="primary", size="lg")
        traction_status = gr.Textbox(
            label="Status",
            value="Configure mapping in Tab 5, then click Calculate.",
            interactive=False
        )
        
        gr.Markdown("### Overall Sample (K=1 Baseline)")
        overall_tbl = gr.Dataframe(
            label="Overall Sample Traction",
            interactive=False
        )
        
        gr.Markdown("---")
        gr.Markdown("### Segment-wise Traction (Transposed for AI Copy-Paste)")
        segment_tbl = gr.Dataframe(
            label="Segment Traction Scores",
            interactive=False
        )
        
        gr.Markdown("### Segment Rankings")
        ranking_txt = gr.Textbox(
            label="Rankings",
            value="",
            lines=10,
            interactive=False
        )
        
        # Individual scoring section
        gr.Markdown("---")
        gr.Markdown("### 👤 Individual-Level Traction Scores")
        gr.Markdown("*Each row gets its own Value, Access, Evidence, and Traction score.*")
        
        individual_tbl = gr.Dataframe(
            label="Individual Scores Preview (first 10 rows)",
            interactive=False,
            wrap=True
        )
        
        gr.Markdown("### Traction Score Distribution by Segment")
        traction_hist = gr.Image(
            label="Histogram",
            type="filepath",
            interactive=False
        )
        
        # Export section
        gr.Markdown("---")
        gr.Markdown("### 📥 Export")
        
        with gr.Row():
            export_report_btn = gr.Button("📄 Download Report (TXT)", variant="secondary", size="sm")
            export_csv_btn = gr.Button("📊 Download Scored Data (CSV)", variant="secondary", size="sm")
        
        export_file = gr.File(label="Download", interactive=False)
        export_status = gr.Textbox(
            label="Export Status",
            value="Calculate traction, then export.",
            interactive=False
        )
    
    # ═════════════════════════════════════════════════════════════════
    # HELPER FUNCTIONS
    # ═════════════════════════════════════════════════════════════════
    
    def parse_weights(weight_text):
        """Parse weight text into dict: var -> {Value: w, Access: w, Evidence: w}."""
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
        """Build weight text from selected variables (default weight=1, no heuristics)."""
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
        """Parse comma-separated names into list of length k."""
        if not names_text:
            return [f"Segment {i+1}" for i in range(k)]
        names = [n.strip() for n in names_text.split(",")]
        while len(names) < k:
            names.append(f"Segment {len(names)+1}")
        return names[:k]
    
    # ═════════════════════════════════════════════════════════════════
    # CALLBACKS — Phase 1 (Tabs 1-4)
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
    
    def handle_confirm(df, selected_basis, selected_cat):
        if df is None or not selected_basis:
            return None, [], None, "❌ Please select basis variables first.", None, None
        
        selected_cat = selected_cat or []
        
        df_proc = df[selected_basis].copy()
        df_proc = df_proc.dropna()
        if len(df_proc) < 2:
            return None, [], None, "❌ Not enough valid rows after dropping missing values.", None, None
        
        for col in selected_cat:
            if col in df_proc.columns:
                dummies = pd.get_dummies(df_proc[col], prefix=col, drop_first=True)
                dummies = dummies.astype(int)
                df_proc = pd.concat([df_proc.drop(columns=[col]), dummies], axis=1)
        
        non_numeric = df_proc.select_dtypes(exclude=[np.number]).columns.tolist()
        if non_numeric:
            return None, [], None, f"❌ Non-numeric columns remain: {non_numeric}", None, None
        
        final_cols = df_proc.columns.tolist()
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_proc.values)
        
        wcss = []
        ks = range(1, min(11, len(X_scaled)))
        for k in ks:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            wcss.append(km.inertia_)
        
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(list(ks), wcss, 'o-', linewidth=2.5, markersize=9, color='#2E86AB')
        
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
        scree_path = "/tmp/scree_plot.png"
        plt.savefig(scree_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        wcss_df = pd.DataFrame({"K": list(ks), "WCSS": [round(w, 2) for w in wcss]})
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
    
    def handle_run(df_proc, processed_cols, X_scaled, k):
        if df_proc is None or X_scaled is None:
            return None, None, None, None, None, "❌ Confirm variables in Tab 2 first.", None, None, None, None
        
        if len(X_scaled) < k:
            return None, None, None, None, None, f"❌ Need ≥{k} rows for K={k}.", None, None, None, None
        
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        
        default_names = [f"Segment {i+1}" for i in range(k)]
        
        cents = pd.DataFrame(
            np.round(km.cluster_centers_, 3).T,
            index=processed_cols,
            columns=default_names
        )
        cents.index.name = "Variable"
        cents = cents.reset_index()
        
        sizes = pd.Series(labels).value_counts().sort_index()
        sizes_df = pd.DataFrame({
            "Segment": [default_names[i] for i in sizes.index],
            "Count": sizes.values,
            "Pct": (sizes.values / len(labels) * 100).round(1)
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
        
        scatter_path = "/tmp/scatter_plot.png"
        plt.savefig(scatter_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        result_df = df_proc.copy()
        result_df["Segment"] = [default_names[l] for l in labels]
        
        return (
            cents,
            sizes_df,
            scatter_path,
            result_df.head(20),
            labels,
            f"✅ K-Means complete! {k} segments. Name them in the field above.",
            ", ".join(default_names),
            gr.CheckboxGroup(choices=processed_cols, value=[], label="Value Variables", interactive=True),
            gr.CheckboxGroup(choices=processed_cols, value=[], label="Access Variables", interactive=True),
            gr.CheckboxGroup(choices=processed_cols, value=[], label="Evidence Variables", interactive=True)
        )
    
    # ── Apply segment names ───────────────────────────────────────────
    def handle_apply_names(names_text, k, labels, df_proc, cents, sizes, scatter_path, labeled_data):
        names = parse_segment_names(names_text, k)
        
        if cents is not None and not cents.empty:
            cents_new = cents.copy()
            old_cols = [c for c in cents_new.columns if c != "Variable"]
            for i, old in enumerate(old_cols):
                if i < len(names):
                    cents_new = cents_new.rename(columns={old: names[i]})
        else:
            cents_new = cents
        
        if sizes is not None and not sizes.empty:
            sizes_new = sizes.copy()
            sizes_new["Segment"] = names[:len(sizes_new)]
        else:
            sizes_new = sizes
        
        if df_proc is not None and labels is not None:
            result_df = df_proc.copy()
            result_df["Segment"] = [names[l] for l in labels]
            labeled_new = result_df.head(20)
        else:
            labeled_new = labeled_data
        
        return names, cents_new, sizes_new, labeled_new, f"✅ Names applied: {', '.join(names)}"
    
    # ── Update weight editor when checkboxes change ─────────────────
    def update_weight_editor(processed_cols, value_vars, access_vars, evidence_vars):
        if not processed_cols:
            return ""
        return build_weight_text(value_vars, access_vars, evidence_vars)
    
    # ── Clear weights ─────────────────────────────────────────────────
    def handle_clear_weights(processed_cols):
        if not processed_cols:
            return "", gr.CheckboxGroup(choices=["(Run segmentation first)"], value=[]), gr.CheckboxGroup(choices=["(Run segmentation first)"], value=[]), gr.CheckboxGroup(choices=["(Run segmentation first)"], value=[])
        return (
            "",
            gr.CheckboxGroup(choices=processed_cols, value=[], label="Value Variables", interactive=True),
            gr.CheckboxGroup(choices=processed_cols, value=[], label="Access Variables", interactive=True),
            gr.CheckboxGroup(choices=processed_cols, value=[], label="Evidence Variables", interactive=True)
        )
    
    # ── Traction calculation (Overall + Segment-wise + Individual) ────
    def handle_traction(df_proc, labels, weight_text, segment_names, df_raw):
        if df_proc is None:
            return "❌ Run segmentation in Tab 3 first.", None, None, "", None, None, None
        
        weights = parse_weights(weight_text)
        if not weights:
            return "❌ Set weights in Tab 5 first. Check variables and assign weights.", None, None, "", None, None, None
        
        value_vars = [v for v, w in weights.items() if w.get("Value", 0) > 0]
        access_vars = [v for v, w in weights.items() if w.get("Access", 0) > 0]
        evidence_vars = [v for v, w in weights.items() if w.get("Evidence", 0) > 0]
        
        if not value_vars or not access_vars or not evidence_vars:
            return "❌ Each component needs at least one variable with weight > 0.", None, None, "", None, None, None
        
        analysis_df = df_proc.copy()
        if labels is not None:
            analysis_df["Segment"] = [segment_names[l] for l in labels] if len(segment_names) > max(labels) else [f"Segment {l+1}" for l in labels]
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
            """Compute scores for a single row (Series)."""
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
        
        # Build scored dataframe
        scored_df = df_proc.copy()
        scored_df["Segment"] = analysis_df["Segment"]
        scored_df["Value_score"] = individual_scores["Value_score"].values
        scored_df["Access_score"] = individual_scores["Access_score"].values
        scored_df["Evidence_score"] = individual_scores["Evidence_score"].values
        scored_df["Traction_quotient"] = individual_scores["Traction_quotient"].values
        
        # Segment rank (1 = best traction mean)
        seg_traction_mean = scored_df.groupby("Segment")["Traction_quotient"].mean().sort_values(ascending=False)
        seg_rank_map = {seg: i+1 for i, seg in enumerate(seg_traction_mean.index)}
        scored_df["Segment_rank"] = scored_df["Segment"].map(seg_rank_map)
        
        # ── Overall Sample ──────────────────────────────────────────
        v_ov = scored_df["Value_score"].mean()
        a_ov = scored_df["Access_score"].mean()
        e_ov = scored_df["Evidence_score"].mean()
        traction_ov = scored_df["Traction_quotient"].mean()
        
        overall_result = pd.DataFrame({
            "Metric": ["Size_Count", "Size_Pct", "Value", "Access", "Evidence", "Traction"],
            "Overall_Sample": [
                len(scored_df),
                100.0,
                round(v_ov, 4),
                round(a_ov, 4),
                round(e_ov, 4),
                round(traction_ov, 4)
            ]
        })
        
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
                    "Size_Pct": round(size_pct, 1),
                    "Value": round(v_s, 3),
                    "Access": round(a_s, 3),
                    "Evidence": round(e_s, 3),
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
                rankings.append(f"   Value={v:.3f} | Access={a:.3f} | Evidence={e:.3f} | Traction={t:.4f}")
                rankings.append("")
            
            ranking_text = "\n".join(rankings)
        else:
            transposed = None
            ranking_text = "No segmentation run yet."
        
        # ── Histogram ───────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(10, 6))
        segments_ordered = seg_df["Segment"].tolist() if labels is not None else ["Overall"]
        colors = plt.cm.Set2(np.linspace(0, 1, len(segments_ordered)))
        
        for i, seg in enumerate(segments_ordered):
            seg_data = scored_df[scored_df["Segment"] == seg]["Traction_quotient"]
            ax.hist(seg_data, bins=30, alpha=0.6, label=seg, color=colors[i], edgecolor='white')
        
        ax.axvline(scored_df["Traction_quotient"].mean(), color='black', linestyle='--', linewidth=2, label=f'Overall Mean={scored_df["Traction_quotient"].mean():.3f}')
        ax.set_xlabel("Traction Quotient", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.set_title("Distribution of Individual Traction Scores by Segment", fontsize=14, fontweight='bold')
        ax.legend(title="Segments", loc='best')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        hist_path = "/tmp/traction_histogram.png"
        plt.savefig(hist_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        # Preview of individual scores
        preview_cols = ["Segment", "Value_score", "Access_score", "Evidence_score", "Traction_quotient", "Segment_rank"]
        if df_raw is not None and len(df_raw.columns) > 0:
            id_col = df_raw.columns[0]
            if id_col in scored_df.columns:
                preview_cols = [id_col] + preview_cols
        
        individual_preview = scored_df[preview_cols].head(10)
        
        return (
            f"✅ Traction computed for {len(scored_df):,} individuals. Overall mean={scored_df['Traction_quotient'].mean():.4f}",
            overall_result,
            transposed,
            ranking_text,
            individual_preview,
            hist_path,
            scored_df
        )
    
    # ── Export report ─────────────────────────────────────────────────
    def handle_export_report(df_proc, labels, segment_names, weight_text, reflection, traction_status, overall_tbl, segment_tbl, ranking_txt):
        if df_proc is None:
            return None, "❌ Run full analysis before exporting."
        
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
            "",
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
            f"**Status:** {traction_status}",
            "",
            "### Overall Sample (K=1 Baseline)",
            "",
        ])
        
        if overall_tbl is not None and not overall_tbl.empty:
            report_lines.append(overall_tbl.to_markdown(index=False))
        
        report_lines.extend([
            "",
            "### Segment-wise Traction",
            "",
        ])
        
        if segment_tbl is not None and not segment_tbl.empty:
            report_lines.append(segment_tbl.to_markdown(index=False))
        
        report_lines.extend([
            "",
            "### Rankings",
            "",
            "```",
            ranking_txt if ranking_txt else "(No rankings)",
            "```",
            "",
            "---",
            "",
            "*End of Report*",
        ])
        
        report_text = "\n".join(report_lines)
        
        report_path = "/tmp/traction_report.txt"
        with open(report_path, "w") as f:
            f.write(report_text)
        
        return report_path, f"✅ Report exported: {report_path}"
    
    # ── Export CSV ────────────────────────────────────────────────────
    def handle_export_csv(scored_df):
        if scored_df is None:
            return None, "❌ Calculate traction first before exporting CSV."
        
        csv_path = "/tmp/scored_data.csv"
        scored_df.to_csv(csv_path, index=False)
        
        return csv_path, f"✅ CSV exported: {csv_path} ({len(scored_df):,} rows, {len(scored_df.columns)} columns)"
    
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
        outputs=[cents_tbl, sizes_tbl, scatter_img, labeled_tbl, segment_labels_state, seg_status, segment_names_input, value_check, access_check, evidence_check]
    )
    
    apply_names_btn.click(
        fn=handle_apply_names,
        inputs=[segment_names_input, k_slider, segment_labels_state, df_processed, cents_tbl, sizes_tbl, scatter_img, labeled_tbl],
        outputs=[segment_names_state, cents_tbl, sizes_tbl, labeled_tbl, names_status]
    )
    
    value_check.change(
        fn=update_weight_editor,
        inputs=[processed_vars, value_check, access_check, evidence_check],
        outputs=weight_editor
    )
    access_check.change(
        fn=update_weight_editor,
        inputs=[processed_vars, value_check, access_check, evidence_check],
        outputs=weight_editor
    )
    evidence_check.change(
        fn=update_weight_editor,
        inputs=[processed_vars, value_check, access_check, evidence_check],
        outputs=weight_editor
    )
    
    clear_weights_btn.click(
        fn=handle_clear_weights,
        inputs=processed_vars,
        outputs=[weight_editor, value_check, access_check, evidence_check]
    )
    
    calc_btn.click(
        fn=handle_traction,
        inputs=[df_processed, segment_labels_state, weight_editor, segment_names_state, df_raw],
        outputs=[traction_status, overall_tbl, segment_tbl, ranking_txt, individual_tbl, traction_hist, scored_df_state]
    )
    
    export_report_btn.click(
        fn=handle_export_report,
        inputs=[df_processed, segment_labels_state, segment_names_state, weight_editor, reflection_box, traction_status, overall_tbl, segment_tbl, ranking_txt],
        outputs=[export_file, export_status]
    )
    
    export_csv_btn.click(
        fn=handle_export_csv,
        inputs=scored_df_state,
        outputs=[export_file, export_status]
    )

# ── Launch ──────────────────────────────────────────────────────────────
app.launch(share=True, debug=True)
