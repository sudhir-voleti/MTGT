# ═══════════════════════════════════════════════════════════════════════
# Caselet 1: 4-Tab Customer Segmentation (ipywidgets) — VERSION 2
# FIXED: Transposed centroids (variables as rows), 4-decimal rounding everywhere
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
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import io
import warnings
warnings.filterwarnings('ignore')

# ── Global State ────────────────────────────────────────────────────────
state = {
    'df_raw': None,
    'df_processed': None,
    'processed_vars': [],
    'X_scaled': None,
    'wcss': None,
    'ks': None
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
# TAB 4: RESULTS
# ═══════════════════════════════════════════════════════════════════════

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
    widgets.HTML("<h4>Segment Sizes & Centroids</h4>"),
    widgets.HBox([sizes_output, cents_output]),
    widgets.HTML("<h4>PCA Scatter Plot</h4>"),
    scatter_output,
    widgets.HTML("<h4>Segmented Data Preview</h4>"),
    labeled_output
])

# ═══════════════════════════════════════════════════════════════════════
# ASSEMBLE TABS
# ═══════════════════════════════════════════════════════════════════════

tabs = widgets.Tab(children=[tab1, tab2, tab3, tab4])
tabs.set_title(0, '📁 Data Preview')
tabs.set_title(1, '🔧 Variable Selection')
tabs.set_title(2, '🎯 Segmentation')
tabs.set_title(3, '📊 Results')

# ═══════════════════════════════════════════════════════════════════════
# CALLBACKS
# ═══════════════════════════════════════════════════════════════════════

def handle_upload(change):
    """CSV upload: load data, populate preview, desc stats, and basis checklist."""
    global state

    if not file_in.value:
        return

    try:
        uploaded = list(file_in.value.values())[0]
        content = uploaded['content']
        df = pd.read_csv(io.BytesIO(content))
        state['df_raw'] = df
        all_cols = df.columns.tolist()

        # HTML preview
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

        # Descriptive stats
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

        # Update basis checklist
        basis_check.options = all_cols
        basis_check.value = ()
        basis_check.disabled = False

        # Reset categorical
        cat_check.options = ['(Select basis variables first)']
        cat_check.value = ()
        cat_check.disabled = True

        summary.value = "Upload CSV and select basis variables."
        confirm_status.value = "<p>Select variables and click Confirm to prepare data.</p>"
        confirm_btn.disabled = True

        # Reset downstream
        run_btn.disabled = True
        seg_status.value = "<p>Confirm variables in Tab 2 first.</p>"

        with scree_output:
            clear_output()
            display(HTML("<p style='color:#888;'>Confirm variables in Tab 2 first to see scree plot.</p>"))
        with wcss_output:
            clear_output()
            display(HTML("<p style='color:#888;'>WCSS table will appear after confirming variables.</p>"))

    except Exception as e:
        status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"
        with preview_output:
            clear_output()
            display(HTML(f"<p style='color:red;'>Error: {str(e)}</p>"))

def handle_basis_change(change):
    """Update categorical options and summary when basis variables change."""
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

    # Update categorical options from selected basis
    cat_check.options = selected_basis
    cat_check.value = ()
    cat_check.disabled = False
    confirm_btn.disabled = False

    # Update summary
    lines = [f"📊 Basis variables: {len(selected_basis)}"]
    for v in selected_basis:
        dtype = str(state['df_raw'][v].dtype)
        n_unique = state['df_raw'][v].nunique()
        lines.append(f"  • {v}: {dtype} | {n_unique} unique values")

    summary.value = "\n".join(lines)

def handle_cat_change(change):
    """Update summary when categorical variables are selected."""
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
    """Confirm selection: create dummies, standardize, compute scree plot."""
    global state

    df = state['df_raw']
    selected_basis = list(basis_check.value)
    selected_cat = list(cat_check.value)

    if df is None or not selected_basis:
        confirm_status.value = "<p style='color:red;'>❌ Please select basis variables first.</p>"
        return

    try:
        # Build processed dataframe
        df_proc = df[selected_basis].copy()
        df_proc = df_proc.dropna()
        if len(df_proc) < 2:
            confirm_status.value = "<p style='color:red;'>❌ Not enough valid rows after dropping missing values.</p>"
            return

        # Create (n-1) dummies for categorical vars
        for col in selected_cat:
            if col in df_proc.columns:
                dummies = pd.get_dummies(df_proc[col], prefix=col, drop_first=True)
                dummies = dummies.astype(int)
                df_proc = pd.concat([df_proc.drop(columns=[col]), dummies], axis=1)

        # Ensure all numeric
        non_numeric = df_proc.select_dtypes(exclude=[np.number]).columns.tolist()
        if non_numeric:
            confirm_status.value = f"<p style='color:red;'>❌ Non-numeric columns remain: {non_numeric}</p>"
            return

        final_cols = df_proc.columns.tolist()
        state['df_processed'] = df_proc
        state['processed_vars'] = final_cols

        # Standardize ONCE here, store for K-Means
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_proc.values)
        state['X_scaled'] = X_scaled

        # Compute scree plot on standardized data
        wcss = []
        ks = range(1, min(11, len(X_scaled)))
        for k in ks:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            wcss.append(km.inertia_)

        state['wcss'] = wcss
        state['ks'] = list(ks)

        # Enhanced scree plot with elbow annotation and % drop
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(list(ks), wcss, 'o-', linewidth=2.5, markersize=9, color='#2E86AB')

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

        # WCSS table
        wcss_df = pd.DataFrame({"K": list(ks), "WCSS": [round(w, 4) for w in wcss]})
        pct_drops = [None] + [round((wcss[i-1] - wcss[i]) / wcss[i-1] * 100, 1) for i in range(1, len(wcss))]
        wcss_df["Pct_Drop"] = pct_drops

        with wcss_output:
            clear_output()
            display(HTML("<p><b>WCSS Values</b></p>"))
            display(wcss_df.style.set_properties(**{'font-size': '11px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#e8f4f8'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        confirm_status.value = f"<p style='color:green;'>✅ Standardized & dummies ready! <b>{len(df_proc):,}</b> rows × <b>{len(final_cols)}</b> columns.</p>"

        # Enable run button
        run_btn.disabled = False
        seg_status.value = "<p>Ready to run segmentation. Choose K and click Run.</p>"

        # Switch to segmentation tab
        tabs.selected_index = 2

    except Exception as e:
        confirm_status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"

def handle_run(b):
    """Run K-Means segmentation on pre-standardized data."""
    global state

    df_proc = state['df_processed']
    X_scaled = state['X_scaled']
    processed_cols = state['processed_vars']
    k = k_slider.value

    if df_proc is None or X_scaled is None:
        seg_status.value = "<p style='color:red;'>❌ Confirm variables in Tab 2 first.</p>"
        return

    if len(X_scaled) < k:
        seg_status.value = f"<p style='color:red;'>❌ Need ≥{k} rows for K={k}.</p>"
        return

    try:
        # K-Means on ALREADY standardized data
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)

        # Centroids — TRANSPOSED for readability (variables as rows, segments as columns)
        cents = pd.DataFrame(
            np.round(km.cluster_centers_, 4).T,
            index=processed_cols,
            columns=[f"Segment {i+1}" for i in range(k)]
        )
        cents.index.name = "Variable"
        cents = cents.reset_index()

        # Segment sizes
        sizes = pd.Series(labels).value_counts().sort_index()
        sizes_df = pd.DataFrame({
            "Segment": [f"Segment {i+1}" for i in sizes.index],
            "Count": sizes.values,
            "Pct": (sizes.values / len(labels) * 100).round(4)
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

        with scatter_output:
            clear_output()
            display(fig)
        plt.close(fig)

        # Display sizes
        with sizes_output:
            clear_output()
            display(HTML("<h4>Segment Sizes</h4>"))
            display(sizes_df.style.set_properties(**{'font-size': '11px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#e8f4f8'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        # Display centroids (transposed) + CSV download
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

        # Labeled data preview
        result_df = df_proc.copy()
        result_df["Segment"] = [f"Segment {l+1}" for l in labels]

        with labeled_output:
            clear_output()
            display(HTML(f"<h4>Segmented Data Preview (showing {min(20, len(result_df))} of {len(result_df)} rows)</h4>"))
            display(result_df.head(20).style.set_properties(**{'font-size': '10px'}).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f0f0f0'), ('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('border', '1px solid #eee')]}
            ]))

        seg_status.value = f"<p style='color:green;'>✅ K-Means complete! <b>{k}</b> segments on <b>{len(df_proc):,}</b> standardized observations.</p>"

        # Switch to results tab
        tabs.selected_index = 3

    except Exception as e:
        seg_status.value = f"<p style='color:red;'>❌ Error: {str(e)}</p>"

# ── Wire up events ────────────────────────────────────────────────────
file_in.observe(handle_upload, names='value')
basis_check.observe(handle_basis_change, names='value')
cat_check.observe(handle_cat_change, names='value')
confirm_btn.on_click(handle_confirm)
run_btn.on_click(handle_run)

# ── Display ───────────────────────────────────────────────────────────
display(widgets.HTML("<h1>🎯 Caselet 1: Customer Segmentation</h1>"))
display(widgets.HTML("<p><b>Upload data, select variables, run K-Means clustering, and explore results.</b></p>"))
display(tabs)
