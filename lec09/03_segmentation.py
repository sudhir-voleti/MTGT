# ═══════════════════════════════════════════════════════════════════
#  STEP 3: Generic Segmentation Tool — v2 with Scree Plot + User K
# ═══════════════════════════════════════════════════════════════════

import io
import numpy as np
import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# =============================================================================
# STATE
# =============================================================================

pw_df = None
psych_df = None
seg_col = None
k_clusters = 3

# =============================================================================
# WIDGETS
# =============================================================================

# --- Source panel ---
use_inherited = widgets.Checkbox(value=False, description='Use Step 2 results', disabled=True)
upload_pw = widgets.FileUpload(accept='.csv', multiple=False, description='📁 Part-Worths', 
                               button_style='primary', layout=widgets.Layout(width='280px'))
upload_psych = widgets.FileUpload(accept='.csv', multiple=False, description='📁 Psychographic (opt)', 
                                  button_style='info', layout=widgets.Layout(width='280px'))
btn_source = widgets.Button(description='▶ Confirm Source', button_style='success')

source_status = widgets.HTML("Upload part-worth CSV from Step 2, or check 'Use Step 2 results' if available.")

source_panel = widgets.VBox([
    widgets.HTML("<h2>Segmentation Tool: Step 1 — Data Source</h2>"),
    widgets.HTML("<p>Part-worths from Step 2 are auto-detected. If unavailable, upload the CSV.</p>"),
    widgets.HBox([use_inherited, upload_pw, upload_psych, btn_source]),
    source_status
])

# --- Mapping panel ---
dd_resp = widgets.Dropdown(options=[], description='Resp ID*:', layout=widgets.Layout(width='260px'))
dd_seg = widgets.Dropdown(options=['-- None --'], description='True Segment:', layout=widgets.Layout(width='260px'))
sel_pw = widgets.SelectMultiple(options=[], description='Part-Worths*:', rows=6, 
                                  layout=widgets.Layout(width='320px', height='200px'))

btn_scree = widgets.Button(description='▶ Show Scree Plot', button_style='info', disabled=True)
sel_k = widgets.IntSlider(value=3, min=2, max=8, description='K:', layout=widgets.Layout(width='200px'))
btn_lock = widgets.Button(description='🔒 Lock & Cluster', button_style='success', disabled=True)
btn_reset = widgets.Button(description='🗑 Reset', button_style='warning')

scree_out = widgets.Output()
mapping_status = widgets.HTML("<i>Confirm data source first.</i>")

mapping_controls = widgets.VBox([
    widgets.HTML("<h3>Step 2 — Configure Clustering</h3>"),
    widgets.HBox([dd_resp, dd_seg]),
    sel_pw,
    widgets.HBox([btn_scree, sel_k, btn_lock, btn_reset]),
    scree_out,
    mapping_status
])

mapping_panel = widgets.VBox([])

# --- Results ---
results_html = widgets.HTML("")
results_panel = widgets.VBox([results_html])
viz_panel = widgets.VBox([])

# =============================================================================
# AUTO-DETECT: Try to grab ib_df from Step 2 namespace
# =============================================================================

try:
    pw_df = ib_df.copy()
    use_inherited.value = True
    use_inherited.disabled = False
    source_status.value = "✅ Auto-detected part-worths from Step 2. Check box and confirm."
except NameError:
    use_inherited.disabled = True
    source_status.value = "ℹ️ No Step 2 results found. Upload part-worth CSV."

# =============================================================================
# EVENT HANDLERS
# =============================================================================

def on_source(_):
    global pw_df, psych_df
    
    if use_inherited.value:
        try:
            pw_df = ib_df.copy()
            source_status.value = f"✅ Using Step 2 results: {pw_df.shape}"
        except NameError:
            source_status.value = "<span style='color:#c53030'>❌ Step 2 results not available. Upload CSV.</span>"
            return
    else:
        if not upload_pw.value:
            source_status.value = "<span style='color:#c53030'>❌ Upload part-worth CSV or check 'Use Step 2 results'</span>"
            return
        raw = list(upload_pw.value.values())[0]['content']
        pw_df = pd.read_csv(io.BytesIO(raw))
        source_status.value = f"✅ Uploaded part-worths: {pw_df.shape}"
    
    # Load psychographic if provided
    if upload_psych.value:
        raw2 = list(upload_psych.value.values())[0]['content']
        psych_df = pd.read_csv(io.BytesIO(raw2))
        source_status.value += f" | Psychographic: {psych_df.shape}"
    else:
        psych_df = None
    
    # Populate mapping
    all_cols = list(pw_df.columns)
    numeric_cols = [c for c in all_cols if pd.api.types.is_numeric_dtype(pw_df[c])]
    
    # Exclude obvious non-part-worth columns
    exclude_patterns = ['resp', 'id', 'subject', 'segment', 'cluster', 'group', 'task', 'profile', 'trial', 'chosen', 'rating', 'y_']
    candidate_pws = []
    for c in numeric_cols:
        low = c.lower()
        if any(p in low for p in exclude_patterns):
            continue
        if c.startswith('d_') or pw_df[c].std() > 0.01:
            candidate_pws.append(c)
    
    dd_resp.options = all_cols
    dd_seg.options = ['-- None --'] + all_cols
    
    resp_guess = next((c for c in all_cols if any(k in c.lower() for k in ['resp', 'id', 'subject'])), all_cols[0])
    seg_guess = next((c for c in all_cols if any(k in c.lower() for k in ['segment', 'cluster', 'group'])), '-- None --')
    
    dd_resp.value = resp_guess
    dd_seg.value = seg_guess if seg_guess in dd_seg.options else '-- None --'
    
    sel_pw.options = numeric_cols
    sel_pw.value = tuple(candidate_pws[:min(12, len(candidate_pws))])
    
    source_status.value += f" | {len(candidate_pws)} candidate part-worths detected."
    
    btn_scree.disabled = False
    btn_lock.disabled = False
    mapping_panel.children = [mapping_controls]

def on_scree(_):
    if len(sel_pw.value) == 0:
        mapping_status.value = "<span style='color:#c53030'>❌ Select part-worth columns first.</span>"
        return
    
    pw_cols = list(sel_pw.value)
    X = pw_df[pw_cols].fillna(0).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    inertias = []
    K_range = range(1, 9)
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
    
    # Suggest elbow
    elbow = 3
    if len(inertias) >= 3:
        deltas = [inertias[i] - inertias[i+1] for i in range(len(inertias)-1)]
        elbow = np.argmax([deltas[i] - deltas[i+1] for i in range(len(deltas)-1)]) + 2
    
    with scree_out:
        clear_output()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(list(K_range), inertias, 'o-', color='#1e40af', linewidth=2, markersize=8)
        ax.set_xlabel('Number of Clusters (K)')
        ax.set_ylabel('Inertia (Within-Cluster Sum of Squares)')
        ax.set_title('Scree Plot: Where is the Elbow?')
        ax.set_xticks(list(K_range))
        
        current_k = sel_k.value
        ax.axvline(current_k, color='#e53e3e', linestyle='--', alpha=0.5, label=f'Current K={current_k}')
        ax.axvline(elbow, color='#16a34a', linestyle='--', alpha=0.5, label=f'Suggested K={elbow}')
        ax.legend()
        
        plt.tight_layout()
        plt.show()
        
        print(f"\nInertia: {dict(zip(K_range, [round(i,1) for i in inertias]))}")
        print(f"Suggested elbow: K={elbow}")
        print("Adjust K slider, then click Lock & Cluster.")

def on_lock(_):
    global seg_col, k_clusters
    
    if len(sel_pw.value) == 0:
        mapping_status.value = "<span style='color:#c53030'>❌ Select part-worth columns.</span>"
        return
    
    k_clusters = sel_k.value
    resp_col = dd_resp.value
    seg_col = dd_seg.value if dd_seg.value != '-- None --' else None
    pw_cols = list(sel_pw.value)
    
    dd_resp.disabled = True
    dd_seg.disabled = True
    sel_pw.disabled = True
    sel_k.disabled = True
    btn_scree.disabled = True
    btn_lock.disabled = True
    
    # K-Means
    X = pw_df[pw_cols].fillna(0).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    pw_df['Cluster'] = clusters
    
    # Results
    lines = []
    lines.append("="*60)
    lines.append(f"K-MEANS CLUSTERING (K={k_clusters})")
    lines.append("="*60)
    lines.append(f"Part-worth columns: {len(pw_cols)}")
    lines.append(f"Respondents: {pw_df[resp_col].nunique()}")
    
    lines.append("\nCluster sizes:")
    sizes = pw_df['Cluster'].value_counts().sort_index()
    for c, n in sizes.items():
        lines.append(f"  Cluster {c}: {n} ({n/len(pw_df)*100:.1f}%)")
    
    if seg_col:
        lines.append(f"\n--- Cross-tab: Cluster vs {seg_col} ---")
        ctab = pd.crosstab(pw_df['Cluster'], pw_df[seg_col])
        lines.append(str(ctab))
        lines.append("\nPurity (best match):")
        for c in sorted(pw_df['Cluster'].unique()):
            seg_dist = pw_df[pw_df['Cluster']==c][seg_col].value_counts()
            if len(seg_dist) > 0:
                purity = seg_dist.iloc[0] / seg_dist.sum() * 100
                lines.append(f"  Cluster {c}: {purity:.1f}% = {seg_dist.index[0]}")
    
    if psych_df is not None and seg_col:
        lines.append("\n--- Psychographic Validation ---")
        psych_merged = psych_df.merge(pw_df[[resp_col, 'Cluster']], on=resp_col, how='left')
        psych_cols = [c for c in psych_merged.columns if c not in [resp_col, 'Cluster', seg_col]]
        if len(psych_cols) > 0:
            psych_by_cluster = psych_merged.groupby('Cluster')[psych_cols].mean()
            lines.append(str(psych_by_cluster.round(2)))
    
    lines.append("\n✅ Clustering complete.")
    results_html.value = "<pre style='font-family:monospace; font-size:13px; line-height:1.5;'>" + "\n".join(lines) + "</pre>"
    
    import builtins
    builtins.pw_df = pw_df
    builtins.kmeans_model = kmeans
    
    render_viz(pw_cols, resp_col)

def on_reset(_):
    global pw_df, psych_df, seg_col, k_clusters
    
    pw_df = None
    psych_df = None
    seg_col = None
    k_clusters = 3
    
    dd_resp.disabled = False
    dd_seg.disabled = False
    sel_pw.disabled = False
    sel_k.disabled = False
    btn_scree.disabled = False
    btn_lock.disabled = False
    
    mapping_status.value = "<i>Confirm data source first.</i>"
    results_html.value = ""
    viz_panel.children = []
    scree_out.clear_output()

def render_viz(pw_cols, resp_col):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Cluster profiles
    ax = axes[0]
    cluster_profiles = pw_df.groupby('Cluster')[pw_cols].mean()
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
    ax.set_title('Cluster Profiles')
    ax.legend(title='Cluster')
    ax.axhline(0, color='gray', linestyle='--', alpha=0.3)
    
    # Plot 2: PCA
    ax = axes[1]
    if len(pw_cols) >= 2:
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(pw_df[pw_cols].fillna(0))
        for cl, color in zip(sorted(pw_df['Cluster'].unique()), colors):
            mask = pw_df['Cluster'] == cl
            ax.scatter(X_pca[mask, 0], X_pca[mask, 1], alpha=0.4, s=30, c=color, label=f'Cluster {cl}')
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
        ax.set_title('Cluster Visualization (PCA)')
        ax.legend(title='Cluster')
    else:
        ax.text(0.5, 0.5, 'Need ≥2 part-worths', ha='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.show()
    
    questions = """
    <div style="background:#fffbeb; border:2px dashed #f59e0b; border-radius:12px; padding:16px; margin:12px 0;">
    <h4 style="margin-top:0; color:#b45309;">Discussion Questions</h4>
    <ol style="color:#78350f;">
    <li><b>Naming:</b> What would you name each cluster based on its profile?</li>
    <li><b>Validation:</b> Do clusters match true segments? If not, why?</li>
    <li><b>Beachhead:</b> Which cluster is your target? Which is the chasm?</li>
    </ol>
    </div>
    """
    viz_panel.children = [widgets.HTML(questions)]

# =============================================================================
# WIRE & ASSEMBLE
# =============================================================================

btn_source.on_click(on_source)
btn_scree.on_click(on_scree)
btn_lock.on_click(on_lock)
btn_reset.on_click(on_reset)

full_ui = widgets.VBox([
    source_panel,
    mapping_panel,
    results_panel,
    viz_panel
])

display(full_ui)
