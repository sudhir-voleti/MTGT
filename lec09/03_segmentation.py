# ═══════════════════════════════════════════════════════════════════
#  STEP 3: Generic Segmentation Tool — Upload + Cluster + Validate
# ═══════════════════════════════════════════════════════════════════

import io
import numpy as np
import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =============================================================================
# STATE
# =============================================================================

pw_df = None       # part-worth data (from Step 2 or uploaded)
psych_df = None    # psychographic data (optional, for validation)
seg_col = None     # optional true segment column
k_clusters = 3

# =============================================================================
# WIDGETS
# =============================================================================

# --- Upload panel ---
upload_pw = widgets.FileUpload(accept='.csv', multiple=False, description='📁 Part-Worths', button_style='primary', layout=widgets.Layout(width='280px'))
upload_psych = widgets.FileUpload(accept='.csv', multiple=False, description='📁 Psychographic (opt)', button_style='info', layout=widgets.Layout(width='280px'))
btn_load = widgets.Button(description='▶ Load', button_style='success')
upload_status = widgets.HTML("Upload part-worth CSV from Step 2, or run Step 2 first.")

upload_panel = widgets.VBox([
    widgets.HTML("<h2>Segmentation Tool: Step 1 — Upload</h2>"),
    widgets.HTML("<p>Required: CSV with respondent IDs and part-worth columns.<br>Optional: psychographic CSV for validation.</p>"),
    widgets.HBox([upload_pw, upload_psych, btn_load]),
    upload_status
])

# --- Mapping panel ---
dd_resp = widgets.Dropdown(options=[], description='Resp ID*:', layout=widgets.Layout(width='260px'))
dd_seg = widgets.Dropdown(options=['-- None --'], description='True Segment:', layout=widgets.Layout(width='260px'))
sel_pw = widgets.SelectMultiple(options=[], description='Part-Worths*:', rows=6, layout=widgets.Layout(width='320px', height='200px'))
sel_k = widgets.IntSlider(value=3, min=2, max=6, description='K clusters:', layout=widgets.Layout(width='300px'))

btn_lock = widgets.Button(description='🔒 Lock & Cluster', button_style='success', disabled=True)
btn_reset = widgets.Button(description='🗑 Reset', button_style='warning')
mapping_status = widgets.HTML("<i>Select Resp ID and part-worth columns, then lock.</i>")

mapping_controls = widgets.VBox([
    widgets.HTML("<h3>Step 2 — Configure Clustering</h3>"),
    widgets.HBox([dd_resp, dd_seg, sel_k]),
    sel_pw,
    widgets.HBox([btn_lock, btn_reset]),
    mapping_status
])

mapping_panel = widgets.VBox([])

# --- Results panel ---
results_html = widgets.HTML("")
results_panel = widgets.VBox([results_html])

viz_panel = widgets.VBox([])

# =============================================================================
# EVENT HANDLERS
# =============================================================================

def on_load(_):
    global pw_df, psych_df
    
    if not upload_pw.value:
        upload_status.value = "<span style='color:#c53030'>❌ Upload part-worth CSV first.</span>"
        return
    
    # Load part-worths
    raw = list(upload_pw.value.values())[0]['content']
    pw_df = pd.read_csv(io.BytesIO(raw))
    
    # Load psychographic if provided
    if upload_psych.value:
        raw2 = list(upload_psych.value.values())[0]['content']
        psych_df = pd.read_csv(io.BytesIO(raw2))
        upload_status.value = f"✅ Part-worths: {pw_df.shape} | Psychographic: {psych_df.shape}"
    else:
        psych_df = None
        upload_status.value = f"✅ Part-worths: {pw_df.shape} (no psychographic uploaded)"
    
    # Populate mapping
    all_cols = list(pw_df.columns)
    numeric_cols = [c for c in all_cols if pd.api.types.is_numeric_dtype(pw_df[c])]
    
    dd_resp.options = all_cols
    dd_seg.options = ['-- None --'] + all_cols
    
    # Auto-guess
    resp_guess = next((c for c in all_cols if any(k in c.lower() for k in ['resp', 'id', 'subject'])), all_cols[0])
    seg_guess = next((c for c in all_cols if any(k in c.lower() for k in ['segment', 'cluster', 'group'])), '-- None --')
    
    dd_resp.value = resp_guess
    dd_seg.value = seg_guess if seg_guess in dd_seg.options else '-- None --'
    
    # Auto-guess part-worths: numeric columns that look like dummies
    pw_guess = [c for c in numeric_cols if c.startswith('d_') or 'part' in c.lower() or 'pw' in c.lower() or 'beta' in c.lower()]
    if not pw_guess:
        pw_guess = [c for c in numeric_cols if c not in [resp_guess, seg_guess]]
    sel_pw.options = numeric_cols
    sel_pw.value = tuple(pw_guess[:min(10, len(pw_guess))])
    
    btn_lock.disabled = False
    mapping_panel.children = [mapping_controls]

def on_lock(_):
    global seg_col, k_clusters
    
    if len(sel_pw.value) == 0:
        mapping_status.value = "<span style='color:#c53030'>❌ Select at least one part-worth column.</span>"
        return
    
    resp_col = dd_resp.value
    seg_col = dd_seg.value if dd_seg.value != '-- None --' else None
    k_clusters = sel_k.value
    pw_cols = list(sel_pw.value)
    
    # Disable
    dd_resp.disabled = True
    dd_seg.disabled = True
    sel_pw.disabled = True
    sel_k.disabled = True
    btn_lock.disabled = True
    
    # Run K-Means
    X = pw_df[pw_cols].fillna(0).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    pw_df['Cluster'] = clusters
    
    # Build results
    lines = []
    lines.append("="*60)
    lines.append(f"K-MEANS CLUSTERING (K={k_clusters})")
    lines.append("="*60)
    lines.append(f"\nPart-worth columns used: {len(pw_cols)}")
    lines.append(f"Respondents: {pw_df[resp_col].nunique()}")
    
    # Cluster sizes
    lines.append("\nCluster sizes:")
    sizes = pw_df['Cluster'].value_counts().sort_index()
    for c, n in sizes.items():
        lines.append(f"  Cluster {c}: {n} ({n/len(pw_df)*100:.1f}%)")
    
    # If true segment available, cross-tab
    if seg_col:
        lines.append(f"\n--- Cross-tab: Cluster vs {seg_col} ---")
        ctab = pd.crosstab(pw_df['Cluster'], pw_df[seg_col])
        lines.append(str(ctab))
        
        # Purity
        lines.append("\nPurity (best match):")
        for c in sorted(pw_df['Cluster'].unique()):
            seg_dist = pw_df[pw_df['Cluster']==c][seg_col].value_counts()
            if len(seg_dist) > 0:
                purity = seg_dist.iloc[0] / seg_dist.sum() * 100
                lines.append(f"  Cluster {c}: {purity:.1f}% are {seg_dist.index[0]}")
    
    # Psychographic validation
    if psych_df is not None and seg_col:
        lines.append("\n--- Psychographic Validation ---")
        # Merge cluster labels into psych data
        psych_merged = psych_df.merge(pw_df[[resp_col, 'Cluster']], on=resp_col, how='left')
        
        psych_cols = [c for c in psych_merged.columns if c not in [resp_col, 'Cluster', seg_col]]
        if len(psych_cols) > 0:
            psych_by_cluster = psych_merged.groupby('Cluster')[psych_cols].mean()
            lines.append(str(psych_by_cluster.round(2)))
    
    lines.append("\n✅ Clustering complete.")
    results_html.value = "<pre style='font-family:monospace; font-size:13px; line-height:1.5;'>" + "\n".join(lines) + "</pre>"
    
    # Store globals
    import builtins
    builtins.pw_df = pw_df
    builtins.kmeans_model = kmeans
    
    # Render viz
    render_viz(pw_cols, resp_col)

def on_reset(_):
    dd_resp.disabled = False
    dd_seg.disabled = False
    sel_pw.disabled = False
    sel_k.disabled = False
    btn_lock.disabled = False
    mapping_status.value = "<i>Select Resp ID and part-worth columns, then lock.</i>"
    results_html.value = ""
    viz_panel.children = []

def render_viz(pw_cols, resp_col):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Cluster profiles (mean part-worths)
    ax = axes[0]
    cluster_profiles = pw_df.groupby('Cluster')[pw_cols].mean()
    
    # Select top 6 most variable part-worths for clarity
    pw_vars = cluster_profiles.std(axis=0).sort_values(ascending=False)
    plot_cols = list(pw_vars.index[:min(6, len(pw_vars))])
    
    x = np.arange(len(plot_cols))
    w = 0.8 / len(cluster_profiles)
    colors = ['#2c7a7b', '#d69e2e', '#e53e3e', '#805ad5', '#dd6b20', '#38a169']
    
    for i, (cl, color) in enumerate(zip(cluster_profiles.index, colors)):
        vals = cluster_profiles.loc[cl, plot_cols].values
        ax.bar(x + i*w, vals, w, label=f'Cluster {cl}', color=color, edgecolor='black')
    
    ax.set_xticks(x + w*(len(cluster_profiles)-1)/2)
    ax.set_xticklabels([c.replace('d_', '').replace('_', ' ')[:15] for c in plot_cols], rotation=30, ha='right')
    ax.set_ylabel('Mean Part-Worth')
    ax.set_title('Cluster Profiles: Mean Part-Worths by Cluster')
    ax.legend(title='Cluster')
    ax.axhline(0, color='gray', linestyle='--', alpha=0.3)
    
    # Plot 2: PCA projection (if enough columns)
    ax = axes[1]
    if len(pw_cols) >= 2:
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(pw_df[pw_cols].fillna(0))
        
        for cl, color in zip(sorted(pw_df['Cluster'].unique()), colors):
            mask = pw_df['Cluster'] == cl
            ax.scatter(X_pca[mask, 0], X_pca[mask, 1], alpha=0.4, s=30, c=color, label=f'Cluster {cl}')
        
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        ax.set_title('Cluster Visualization (PCA)')
        ax.legend(title='Cluster')
    else:
        ax.text(0.5, 0.5, 'Need ≥2 part-worths for PCA', ha='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.show()
    
    # Socratic questions
    questions = """
    <div style="background:#fffbeb; border:2px dashed #f59e0b; border-radius:12px; padding:16px; margin:12px 0;">
    <h4 style="margin-top:0; color:#b45309;">Discussion Questions</h4>
    <ol style="color:#78350f;">
    <li><b>Naming:</b> Look at the cluster profiles. What would you name each cluster?</li>
    <li><b>Validation:</b> If you have true segments, do clusters match? If not, why?</li>
    <li><b>Psychographics:</b> Do the psychographic means align with your cluster names?</li>
    <li><b>Action:</b> Which cluster is your beachhead? Which is the chasm?</li>
    </ol>
    </div>
    """
    viz_panel.children = [widgets.HTML(questions)]

# =============================================================================
# WIRE & ASSEMBLE
# =============================================================================

btn_load.on_click(on_load)
btn_lock.on_click(on_lock)
btn_reset.on_click(on_reset)

full_ui = widgets.VBox([
    upload_panel,
    mapping_panel,
    results_panel,
    viz_panel
])

display(full_ui)
