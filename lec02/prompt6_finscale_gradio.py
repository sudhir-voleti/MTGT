# ═══════════════════════════════════════════════════════════════════════
# App 2: Panel Traction Over Time — Dynamic Account Scoring
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime

# ── Build app ───────────────────────────────────────────────────────────

with gr.Blocks(title="Panel Traction: Dynamic Account Scoring", theme=gr.themes.Soft()) as app:
    
    gr.Markdown("""
    # 📈 Panel Traction: Dynamic Account Scoring
    **Upload panel data, compute monthly traction, cluster trajectories, and visualize dynamics.**
    """)
    
    # ── States ──────────────────────────────────────────────────────────
    df_raw = gr.State(None)
    df_processed = gr.State(None)
    account_id_col = gr.State(None)
    period_col = gr.State(None)
    scored_long = gr.State(None)
    scored_wide = gr.State(None)
    cluster_labels = gr.State(None)
    
    # ═════════════════════════════════════════════════════════════════
    # TAB 1: Upload & Configure
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("📁 Upload & Configure"):
        with gr.Row():
            with gr.Column(scale=1):
                file_in = gr.File(
                    label="Upload Panel CSV",
                    file_types=[".csv"],
                    type="filepath"
                )
                status = gr.Textbox(
                    label="Status",
                    value="Waiting for panel CSV upload...",
                    interactive=False
                )
            
            with gr.Column(scale=2):
                gr.Markdown("### Data Preview")
                html_preview = gr.HTML(
                    value="<p style='color:#888;'>Upload a panel CSV to see preview.</p>"
                )
        
        gr.Markdown("---")
        gr.Markdown("### Panel Configuration")
        
        with gr.Row():
            with gr.Column(scale=1):
                account_dropdown = gr.Dropdown(
                    choices=["(Upload CSV first)"],
                    value="(Upload CSV first)",
                    label="Account ID Field",
                    interactive=False
                )
            
            with gr.Column(scale=1):
                period_dropdown = gr.Dropdown(
                    choices=["(Upload CSV first)"],
                    value="(Upload CSV first)",
                    label="Period Field (Month/Time)",
                    interactive=False
                )
        
        gr.Markdown("### Dataset Overview")
        desc_stats = gr.Textbox(
            label="Descriptive Statistics",
            value="Upload CSV and configure fields.",
            lines=8,
            interactive=False
        )
        
        configure_btn = gr.Button("✅ Configure Panel", variant="primary", size="lg")
        config_status = gr.Textbox(
            label="Configuration Status",
            value="Upload and select fields first.",
            interactive=False
        )
    
    # ═════════════════════════════════════════════════════════════════
    # TAB 2: Map Traction Components
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("🔧 Map Traction Components"):
        
        gr.Markdown("""
        ## Map Variables to Traction Components
        **Step 1:** Check variables for Value, Access, Evidence.
        **Step 2:** Reflect on your mapping.
        **Step 3:** Set weights (default = 1 for checked variables).
        """)
        
        gr.Markdown("### Step 1: Select Variables per Component")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("**Value** (utility, stickiness, usage)")
                value_check = gr.CheckboxGroup(
                    choices=["(Configure panel first)"],
                    label="Value Variables",
                    interactive=False
                )
            
            with gr.Column(scale=1):
                gr.Markdown("**Access** (channel efficiency, reach)")
                access_check = gr.CheckboxGroup(
                    choices=["(Configure panel first)"],
                    label="Access Variables",
                    interactive=False
                )
            
            with gr.Column(scale=1):
                gr.Markdown("**Evidence** (behavioral velocity, conversion)")
                evidence_check = gr.CheckboxGroup(
                    choices=["(Configure panel first)"],
                    label="Evidence Variables",
                    interactive=False
                )
        
        gr.Markdown("---")
        gr.Markdown("### Step 2: 📝 Reflect on Your Mapping")
        
        reflection_box = gr.Textbox(
            label="Your Reflection",
            value="",
            lines=4,
            interactive=True
        )
        
        gr.Markdown("---")
        gr.Markdown("### Step 3: Set Weights")
        gr.Markdown("*Format: `variable_name=Component:weight` one per line. Auto-populates with weight=1.*")
        
        weight_editor = gr.Textbox(
            label="Weights (var=Component:weight, one per line)",
            value="",
            lines=8,
            interactive=True
        )
        
        with gr.Row():
            clear_weights_btn = gr.Button("🔄 Clear All", size="sm")
        
        mapping_status = gr.Textbox(
            label="Mapping Status",
            value="Configure panel in Tab 1 first.",
            interactive=False
        )
    
    # ═════════════════════════════════════════════════════════════════
    # TAB 3: Traction Over Time
    # ═════════════════════════════════════════════════════════════════
    with gr.Tab("📈 Traction Over Time"):
        
        gr.Markdown("""
        ## Compute Traction, Cluster Trajectories, Visualize Dynamics
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Clustering")
                k_slider = gr.Slider(
                    minimum=2, maximum=6, step=1, value=3,
                    label="Number of Trajectory Clusters (K)"
                )
                
                run_btn = gr.Button("📊 Compute & Cluster", variant="primary", size="lg")
                
                run_status = gr.Textbox(
                    label="Status",
                    value="Map variables in Tab 2, then click Compute.",
                    interactive=False
                )
            
            with gr.Column(scale=2):
                gr.Markdown("### Scree Plot (Trajectory Clusters)")
                scree_img = gr.Image(
                    label="WCSS by K",
                    type="filepath",
                    interactive=False
                )
        
        gr.Markdown("---")
        gr.Markdown("### Trajectory Cluster Centroids")
        gr.Markdown("*Mean traction quotient per month for each cluster*")
        
        centroids_tbl = gr.Dataframe(
            label="Cluster Centroids (Traction by Month)",
            interactive=False
        )
        
        gr.Markdown("---")
        gr.Markdown("### Trajectory Plot")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("**Select View**")
                view_dropdown = gr.Dropdown(
                    choices=["Cluster Means", "Full Sample"],
                    value="Cluster Means",
                    label="View",
                    interactive=True
                )
                
                account_dropdown_view = gr.Dropdown(
                    choices=["(Run compute first)"],
                    value="(Run compute first)",
                    label="Select Account (optional)",
                    interactive=False
                )
            
            with gr.Column(scale=2):
                trajectory_img = gr.Image(
                    label="Traction Trajectories",
                    type="filepath",
                    interactive=False
                )
        
        gr.Markdown("---")
        gr.Markdown("### Account-Level Summary")
        
        summary_tbl = gr.Dataframe(
            label="Account Trajectory Summary",
            interactive=False
        )
        
        gr.Markdown("---")
        gr.Markdown("### 📥 Export")
        
        with gr.Row():
            export_wide_btn = gr.Button("📊 Download Wide Format (CSV)", variant="secondary", size="sm")
            export_long_btn = gr.Button("📊 Download Long Format (CSV)", variant="secondary", size="sm")
            export_report_btn = gr.Button("📄 Download Report (TXT)", variant="secondary", size="sm")
        
        export_file = gr.File(label="Download", interactive=False)
        export_status = gr.Textbox(
            label="Export Status",
            value="Compute traction, then export.",
            interactive=False
        )
    
    # ═════════════════════════════════════════════════════════════════
    # HELPER FUNCTIONS
    # ═════════════════════════════════════════════════════════════════
    
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
    
    # ═════════════════════════════════════════════════════════════════
    # CALLBACKS
    # ═════════════════════════════════════════════════════════════════
    
    def handle_upload(fp):
        if fp is None:
            return (
                None,
                "<p style='color:#888;'>Upload a panel CSV to see preview.</p>",
                gr.Dropdown(choices=["(Upload CSV first)"], value="(Upload CSV first)", interactive=False),
                gr.Dropdown(choices=["(Upload CSV first)"], value="(Upload CSV first)", interactive=False),
                "Waiting for CSV upload...",
                "Upload and select fields."
            )
        
        try:
            df = pd.read_csv(fp)
            cols = df.columns.tolist()
            
            likely_account = [c for c in cols if any(x in c.lower() for x in ["account", "id", "tenant", "customer", "user"])]
            likely_period = [c for c in cols if any(x in c.lower() for x in ["period", "month", "time", "week", "quarter"])]
            
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
            
            return (
                df,
                styled_html,
                gr.Dropdown(choices=cols, value=likely_account[0] if likely_account else cols[0], label="Account ID Field", interactive=True),
                gr.Dropdown(choices=cols, value=likely_period[0] if likely_period else cols[0], label="Period Field", interactive=True),
                f"✅ Loaded: {len(df):,} rows",
                "\n".join(stats_lines)
            )
            
        except Exception as e:
            return (
                None,
                f"<p style='color:red;'>Error: {str(e)}</p>",
                gr.Dropdown(choices=["(Error)"], value="(Error)", interactive=False),
                gr.Dropdown(choices=["(Error)"], value="(Error)", interactive=False),
                f"❌ Error: {str(e)}",
                "Error loading file."
            )
    
    def handle_configure(df, account_col, period_col):
        if df is None or not account_col or not period_col:
            return None, None, None, None, "❌ Select both fields."
        
        if account_col == period_col:
            return None, None, None, None, "❌ Account and Period fields must be different."
        
        n_accounts = df[account_col].nunique()
        n_periods = df[period_col].nunique()
        numeric_cols = [c for c in df.columns if c not in [account_col, period_col] and pd.api.types.is_numeric_dtype(df[c])]
        
        if len(numeric_cols) < 2:
            return None, None, None, None, "❌ Need at least 2 numeric variables for traction mapping."
        
        return (
            df,
            account_col,
            period_col,
            gr.CheckboxGroup(choices=numeric_cols, value=[], label="Value Variables", interactive=True),
            gr.CheckboxGroup(choices=numeric_cols, value=[], label="Access Variables", interactive=True),
            gr.CheckboxGroup(choices=numeric_cols, value=[], label="Evidence Variables", interactive=True),
            f"✅ Panel configured: {n_accounts:,} accounts × {n_periods:,} periods. {len(numeric_cols)} numeric variables available."
        )
    
    def update_weight_editor(processed_cols, value_vars, access_vars, evidence_vars):
        # processed_cols is a DataFrame, check if it's None or empty
        if processed_cols is None or (isinstance(processed_cols, pd.DataFrame) and processed_cols.empty):
            return ""
        return build_weight_text(value_vars, access_vars, evidence_vars)

    def handle_clear_weights(processed_cols):
        if processed_cols is None or (isinstance(processed_cols, pd.DataFrame) and processed_cols.empty):
            return "", gr.CheckboxGroup(choices=["(Configure panel first)"], value=[]),   
        return (
            "",
            gr.CheckboxGroup(choices=processed_cols, value=[], label="Value Variables", interactive=True),
            gr.CheckboxGroup(choices=processed_cols, value=[], label="Access Variables", interactive=True),
            gr.CheckboxGroup(choices=processed_cols, value=[], label="Evidence Variables", interactive=True)
        )
    
    def handle_compute(df, account_col, period_col, weight_text, k):
        if df is None or not account_col or not period_col:
            return "❌ Configure panel in Tab 1 first.", None, None, None, None, None, None, None
        
        weights = parse_weights(weight_text)
        if not weights:
            return "❌ Set weights in Tab 2 first.", None, None, None, None, None, None, None
        
        value_vars = [v for v, w in weights.items() if w.get("Value", 0) > 0]
        access_vars = [v for v, w in weights.items() if w.get("Access", 0) > 0]
        evidence_vars = [v for v, w in weights.items() if w.get("Evidence", 0) > 0]
        
        if not value_vars or not access_vars or not evidence_vars:
            return "❌ Each component needs at least one variable with weight > 0.", None, None, None, None, None, None, None
        
        # Row-level traction scoring
        numeric_cols = [c for c in df.columns if c not in [account_col, period_col] and pd.api.types.is_numeric_dtype(df[c])]
        
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
        
        scored_long_df = df.copy()
        scored_long_df["Value_score"] = scores["Value_score"].values
        scored_long_df["Access_score"] = scores["Access_score"].values
        scored_long_df["Evidence_score"] = scores["Evidence_score"].values
        scored_long_df["Traction_quotient"] = scores["Traction_quotient"].values
        
        # Reshape to wide: account × period
        wide = scored_long_df.pivot(index=account_col, columns=period_col, values="Traction_quotient")
        wide.columns = [f"Period_{c}" for c in wide.columns]
        wide = wide.reset_index()
        # Handle missing periods — only fill numeric columns
        numeric_period_cols = [c for c in wide.columns if c.startswith("Period_")]
        wide[numeric_period_cols] = wide[numeric_period_cols].fillna(wide[numeric_period_cols].mean())
        
        # Cluster on trajectory matrix
        X = wide.drop(columns=[account_col]).values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Scree plot
        wcss = []
        ks = range(1, min(7, len(X)))
        for ki in ks:
            km = KMeans(n_clusters=ki, random_state=42, n_init=10)
            km.fit(X_scaled)
            wcss.append(km.inertia_)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(list(ks), wcss, 'bo-', linewidth=2, markersize=8)
        ax.set_xlabel('K (Number of Clusters)', fontsize=12)
        ax.set_ylabel('WCSS', fontsize=12)
        ax.set_title('Scree Plot: Trajectory Clusters', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(list(ks))
        plt.tight_layout()
        scree_path = "/tmp/panel_scree.png"
        plt.savefig(scree_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        # Fit final K-Means
        km_final = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km_final.fit_predict(X_scaled)
        wide["Cluster"] = labels
        
        # Cluster centroids
        centroids = pd.DataFrame(
            km_final.cluster_centers_,
            columns=[f"Period_{c}" for c in sorted(df[period_col].unique())]
        )
        centroids.index = [f"Cluster {i+1}" for i in range(k)]
        centroids = centroids.reset_index().rename(columns={"index": "Cluster"})
        for col in centroids.columns:
            if col != "Cluster":
                centroids[col] = centroids[col].round(4)
        
        # Account-level summary
        summary = wide.copy()
        period_cols = [c for c in summary.columns if c.startswith("Period_")]
        summary["Mean_Traction"] = summary[period_cols].mean(axis=1).round(4)
        summary["Std_Traction"] = summary[period_cols].std(axis=1).round(4)
        summary["Trend"] = (summary[period_cols[-1]] - summary[period_cols[0]]).round(4)
        summary["Cluster"] = [f"Cluster {l+1}" for l in labels]
        
        summary_display = summary[[account_col, "Cluster", "Mean_Traction", "Std_Traction", "Trend"] + period_cols[:3] + period_cols[-3:]]
        
        # Account dropdown (limit to 100 for performance)
        account_list = ["(None)"] + sorted(df[account_col].unique().tolist())[:100]
        
        return (
            f"✅ Computed traction for {len(df):,} rows. Clustered {len(wide):,} accounts into {k} trajectory clusters.",
            scree_path,
            centroids,
            None,
            summary_display,
            scored_long_df,
            wide,
            gr.Dropdown(choices=account_list, value="(None)", label="Select Account", interactive=True)
        )
    
    def handle_trajectory_plot(wide_df, view, account, k, cluster_labels_state):
        if wide_df is None:
            return None
        
        period_cols = [c for c in wide_df.columns if c.startswith("Period_")]
        periods = [int(c.split("_")[1]) for c in period_cols]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if view == "Cluster Means":
            colors = plt.cm.Set2(np.linspace(0, 1, k))
            for i in range(k):
                cluster_data = wide_df[wide_df["Cluster"] == i]
                mean_traj = cluster_data[period_cols].mean()
                ax.plot(periods, mean_traj, 'o-', linewidth=2.5, markersize=8, 
                       color=colors[i], label=f"Cluster {i+1} (n={len(cluster_data)})")
            ax.set_title("Traction Trajectory by Cluster", fontsize=14, fontweight='bold')
        
        elif view == "Full Sample":
            mean_traj = wide_df[period_cols].mean()
            std_traj = wide_df[period_cols].std()
            ax.plot(periods, mean_traj, 'o-', linewidth=2.5, markersize=8, color='#2E86AB', label="Full Sample Mean")
            ax.fill_between(periods, mean_traj - std_traj, mean_traj + std_traj, alpha=0.2, color='#2E86AB', label="±1 SD")
            ax.set_title("Full Sample Traction Trajectory", fontsize=14, fontweight='bold')
        
        # Overlay selected account
        account_col = [c for c in wide_df.columns if not c.startswith("Period_") and c != "Cluster"][0]
        if account and account != "(None)" and account in wide_df[account_col].values:
            acc_data = wide_df[wide_df[account_col] == account]
            if len(acc_data) > 0:
                acc_traj = acc_data[period_cols].values[0]
                ax.plot(periods, acc_traj, 's--', linewidth=2, markersize=10, 
                       color='red', label=f"Account {account}", zorder=5)
        
        ax.set_xlabel("Period", fontsize=12)
        ax.set_ylabel("Traction Quotient", fontsize=12)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        traj_path = "/tmp/trajectory_plot.png"
        plt.savefig(traj_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        return traj_path
    
    def handle_export_wide(wide_df):
        if wide_df is None:
            return None, "❌ Compute traction first."
        path = "/tmp/panel_traction_wide.csv"
        wide_df.to_csv(path, index=False)
        return path, f"✅ Wide format: {path} ({len(wide_df):,} accounts)"
    
    def handle_export_long(long_df):
        if long_df is None:
            return None, "❌ Compute traction first."
        path = "/tmp/panel_traction_long.csv"
        long_df.to_csv(path, index=False)
        return path, f"✅ Long format: {path} ({len(long_df):,} rows)"
    
    def handle_export_report(wide_df, long_df, reflection, centroids, k):
        if wide_df is None:
            return None, "❌ Compute traction first."
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = [
            "# Panel Traction Audit Report",
            "",
            f"Generated: {timestamp}",
            f"Accounts: {len(wide_df):,}",
            f"Clusters: {k}",
            "",
            "---",
            "",
            "## Cluster Centroids (Traction by Period)",
            "",
        ]
        
        if centroids is not None and not centroids.empty:
            report.append(centroids.to_string(index=False))
        
        report.extend([
            "",
            "---",
            "",
            "## Reflection",
            "",
            reflection if reflection else "(No reflection provided)",
            "",
            "---",
            "",
            "*End of Report*"
        ])
        
        path = "/tmp/panel_traction_report.txt"
        with open(path, "w") as f:
            f.write("\n".join(report))
        
        return path, f"✅ Report: {path}"
    
    # ═════════════════════════════════════════════════════════════════
    # WIRE UP
    # ═════════════════════════════════════════════════════════════════
    
    file_in.change(
        fn=handle_upload,
        inputs=file_in,
        outputs=[df_raw, html_preview, account_dropdown, period_dropdown, status, desc_stats]
    )
    
    configure_btn.click(
        fn=handle_configure,
        inputs=[df_raw, account_dropdown, period_dropdown],
        outputs=[df_processed, account_id_col, period_col, value_check, access_check, evidence_check, config_status]
    )
    
    value_check.change(
        fn=update_weight_editor,
        inputs=[df_processed, value_check, access_check, evidence_check],
        outputs=weight_editor
    )
    access_check.change(
        fn=update_weight_editor,
        inputs=[df_processed, value_check, access_check, evidence_check],
        outputs=weight_editor
    )
    evidence_check.change(
        fn=update_weight_editor,
        inputs=[df_processed, value_check, access_check, evidence_check],
        outputs=weight_editor
    )
    
    clear_weights_btn.click(
        fn=handle_clear_weights,
        inputs=df_processed,
        outputs=[weight_editor, value_check, access_check, evidence_check]
    )
    
    run_btn.click(
        fn=handle_compute,
        inputs=[df_processed, account_id_col, period_col, weight_editor, k_slider],
        outputs=[run_status, scree_img, centroids_tbl, trajectory_img, summary_tbl, scored_long, scored_wide, account_dropdown_view]
    )
    
    view_dropdown.change(
        fn=handle_trajectory_plot,
        inputs=[scored_wide, view_dropdown, account_dropdown_view, k_slider, cluster_labels],
        outputs=trajectory_img
    )
    account_dropdown_view.change(
        fn=handle_trajectory_plot,
        inputs=[scored_wide, view_dropdown, account_dropdown_view, k_slider, cluster_labels],
        outputs=trajectory_img
    )
    
    export_wide_btn.click(
        fn=handle_export_wide,
        inputs=scored_wide,
        outputs=[export_file, export_status]
    )
    
    export_long_btn.click(
        fn=handle_export_long,
        inputs=scored_long,
        outputs=[export_file, export_status]
    )
    
    export_report_btn.click(
        fn=handle_export_report,
        inputs=[scored_wide, scored_long, reflection_box, centroids_tbl, k_slider],
        outputs=[export_file, export_status]
    )

# ── Launch ──────────────────────────────────────────────────────────────
app.launch(share=True, debug=True)
