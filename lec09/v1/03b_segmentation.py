# -*- coding: utf-8 -*-
"""
Lec09 — Step 3b Code: K-Means Segmentation on Part-Worths (Generic)
Pure code cell. Run AFTER 03b_theory.py in a separate Colab cell.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/03b_segmentation.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

_state = {'ib_df': None}

# =============================================================================
# 1. Retrieve ib_df or prompt for upload
# =============================================================================

if 'ib_df' in globals():
    _state['ib_df'] = globals()['ib_df']
    print("✓ Using ib_df from Step 3")
    proceed = True
else:
    print("⚠ ib_df not found. Please upload your individual part-worths CSV below:")
    proceed = False

    upload_widget = widgets.FileUpload(accept='.csv', multiple=False, description='Upload Part-Worths CSV')
    def on_upload(change):
        if not upload_widget.value:
            return
        file_info = list(upload_widget.value.values())[0]
        with open('/tmp/ib.csv', 'wb') as f:
            f.write(file_info['content'])
        ib_df = pd.read_csv('/tmp/ib.csv')
        _state['ib_df'] = ib_df
        globals()['ib_df'] = ib_df
        clear_output(wait=True)
        print(f"✓ Loaded {len(ib_df)} respondent part-worth profiles")
        show_run_button()
    upload_widget.observe(on_upload, names='value')
    display(upload_widget)

# =============================================================================
# 2. Expectation + Run Segmentation button
# =============================================================================

def show_run_button():
    print("\n📋 What will happen when you click 'Run Segmentation':")
    print("   • Compute elbow plot (K = 2 to 6) to find optimal number of segments")
    print("   • Run K-Means with K = 3 (or your chosen K)")
    print("   • Show cluster × segment cross-tab (if ground truth available)")
    print("   • Display cluster mean part-worth profiles")
    print("   • Estimated runtime: ~5 seconds")
    print()

    run_btn = widgets.Button(
        description="▶ Run Segmentation",
        button_style='primary',
        layout=widgets.Layout(width='200px', height='40px')
    )
    run_btn.on_click(lambda b: run_segmentation())
    display(run_btn)

# =============================================================================
# 3. Main segmentation analysis
# =============================================================================

def run_segmentation():
    ib_df = _state['ib_df']

    clear_output(wait=True)
    print("="*60)
    print("SEGMENTATION ANALYSIS")
    print("="*60)

    pw_cols = [c for c in ib_df.columns if c not in ['RespID', 'Segment', 'Intercept', 'Cluster']]

    pw_matrix = ib_df[pw_cols].fillna(0)
    scaler = StandardScaler()
    pw_scaled = scaler.fit_transform(pw_matrix)

    # -------------------------------------------------------------------------
    # 3a. Elbow plot
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("ELBOW PLOT: Choosing K")
    print("="*60)

    inertias = []
    K_range = range(2, 7)
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(pw_scaled)
        inertias.append(km.inertia_)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(list(K_range), inertias, 'o-', color='#003366', linewidth=2, markersize=8)
    ax.axvline(x=3, color='#E37222', linestyle='--', linewidth=2, label='K=3 (ground truth)')
    ax.set_xlabel('Number of Clusters (K)', fontsize=12)
    ax.set_ylabel('Inertia (Within-cluster SSE)', fontsize=12)
    ax.set_title('Elbow Plot: How Many Segments?', fontsize=13, color='#003366')
    ax.set_xticks(list(K_range))
    ax.legend()
    plt.tight_layout()
    plt.show()

    print("\nLook for the 'elbow' — where the curve bends. That is your optimal K.")

    # -------------------------------------------------------------------------
    # 3b. K-Means at K=3
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("K-MEANS CLUSTERING (K = 3)")
    print("="*60)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(pw_scaled)
    ib_df['Cluster'] = clusters

    print(f"✓ Clustered {len(ib_df)} respondents into 3 segments")
    print(f"   Cluster sizes: {dict(pd.Series(clusters).value_counts().sort_index())}")

    # Cross-tab with ground truth
    if 'Segment' in ib_df.columns:
        print("\nCluster × True Segment cross-tab:")
        crosstab = pd.crosstab(ib_df['Cluster'], ib_df['Segment'])
        print(crosstab)

        print("\nPurity (best possible mapping):")
        for seg in sorted(ib_df['Segment'].unique()):
            vc = ib_df[ib_df['Segment'] == seg]['Cluster'].value_counts()
            purity = vc.iloc[0] / vc.sum() * 100
            print(f"  {seg:12s}: {purity:5.1f}% in Cluster {vc.index[0]}  ({vc.iloc[0]}/{vc.sum()})")

    # -------------------------------------------------------------------------
    # 3c. Cluster profiles
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("CLUSTER PROFILES: Mean Part-Worths")
    print("="*60)

    cluster_profiles = ib_df.groupby('Cluster')[pw_cols].mean()
    print(cluster_profiles.round(2))

    # Visual: heatmap-style bar chart for each cluster
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for idx, cl in enumerate(sorted(ib_df['Cluster'].unique())):
        row = cluster_profiles.loc[cl]
        vals = row.values
        names = row.index
        colors = ['#E37222' if v > 0 else '#64748b' for v in vals]
        axes[idx].barh(names, vals, color=colors, edgecolor='white')
        axes[idx].set_title(f'Cluster {cl} Profile', fontsize=12, color='#003366')
        axes[idx].axvline(x=0, color='gray', linewidth=0.8)
        axes[idx].set_xlabel('Mean Part-worth', fontsize=9)
    plt.tight_layout()
    plt.show()

    globals()['cluster_profiles'] = cluster_profiles

    # -------------------------------------------------------------------------
    # 3d. Scribble pause
    # -------------------------------------------------------------------------

    display(HTML("""
    <style>
      .caselet-body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; 
                      font-size: 15px; line-height: 1.55; color: #1e293b; max-width: 860px; margin: 0 auto; }
      .caselet-body h2 { font-size: 1.2em; color: #003366; border-bottom: 2px solid #E37222; 
                         padding-bottom: 4px; margin-top: 28px; }
      .caselet-body .pause-box { background: #fffbeb; border: 1px dashed #d97706; 
                                 padding: 16px 18px; margin: 22px 0; }
      .caselet-body .pause-box h3 { font-size: 1.05em; color: #003366; margin-top: 0; }
      .caselet-body textarea { width: 100%; min-height: 50px; padding: 8px 10px; 
                                border: 1px solid #cbd5e1; border-radius: 6px; 
                                font-family: inherit; font-size: 14px; box-sizing: border-box; resize: vertical; }
      .caselet-body .scribble-table th { background-color: #475569; color: white; 
                                          font-size: 13.5px; padding: 9px 12px; text-align: left; }
      .caselet-body .scribble-table td { padding: 8px 12px; vertical-align: top; border: 1px solid #d0d7de; }
    </style>
    <div class="caselet-body">
      <div class="pause-box">
        <h3>Pause and Reflect: Name Your Personas</h3>
        <p>You now have 3 clusters. Each is a buyer persona with distinct preferences. Before you see the true segment labels (if available), name them yourself.</p>
        <table class="scribble-table">
          <thead>
            <tr><th>Cluster</th><th>My Name</th><th>Top 2 Valued Attributes</th><th>Bottom 1 Attribute</th><th>Ideal Product</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>Cluster 0</td>
              <td><textarea placeholder="e.g., The Pragmatists..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
              <td><textarea placeholder="e.g., 110km + Honda + 300 cities..."></textarea></td>
            </tr>
            <tr>
              <td>Cluster 1</td>
              <td><textarea placeholder="e.g., The Tech Enthusiasts..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
            </tr>
            <tr>
              <td>Cluster 2</td>
              <td><textarea placeholder="e.g., The Price Hunters..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top:12px;"><strong>Next:</strong> Run 03c_explore.py to build custom scatterplots and see how these personas are distributed in part-worth space. Or proceed to 04_cbc_mnl.py to validate with choice data.</p>
      </div>
    </div>
    """))

if proceed:
    show_run_button()
