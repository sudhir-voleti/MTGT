# -*- coding: utf-8 -*-
"""
Lec09 — Step 3c Code: Scatterplot Explorer (Generic)
Pure code cell. Run AFTER 03c_theory.py in a separate Colab cell.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/03c_explore.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
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
        show_controls()
    upload_widget.observe(on_upload, names='value')
    display(upload_widget)

# =============================================================================
# 2. Build scatterplot controls
# =============================================================================

def show_controls():
    ib_df = _state['ib_df']

    pw_cols = [c for c in ib_df.columns if c not in ['RespID', 'Segment', 'Intercept', 'Cluster']]

    # Default: pick two highest-variance columns
    variances = ib_df[pw_cols].var().sort_values(ascending=False)
    default_x = variances.index[0] if len(variances) > 0 else pw_cols[0]
    default_y = variances.index[1] if len(variances) > 1 else pw_cols[1] if len(pw_cols) > 1 else pw_cols[0]

    color_options = ['None']
    if 'Cluster' in ib_df.columns:
        color_options.append('Cluster')
    if 'Segment' in ib_df.columns:
        color_options.append('Segment (True)')

    dd_x = widgets.Dropdown(options=pw_cols, value=default_x, description='X-axis:', layout=widgets.Layout(width='350px'))
    dd_y = widgets.Dropdown(options=pw_cols, value=default_y, description='Y-axis:', layout=widgets.Layout(width='350px'))
    dd_color = widgets.Dropdown(options=color_options, value=color_options[-1] if len(color_options) > 1 else 'None', 
                                description='Color by:', layout=widgets.Layout(width='350px'))

    print("\n📋 About to show: interactive scatterplot builder")
    print("   Pick any two part-worth coefficients as axes.")
    print("   Color by cluster or true segment to see how personas separate.")
    print("   Output: scatterplot + Pearson correlation + interpretation.")
    print()

    build_btn = widgets.Button(
        description="▶ Build Scatterplot",
        button_style='primary',
        layout=widgets.Layout(width='200px', height='40px')
    )

    def on_build(b):
        build_scatter(dd_x.value, dd_y.value, dd_color.value)

    build_btn.on_click(on_build)
    display(widgets.VBox([dd_x, dd_y, dd_color, build_btn]))

# =============================================================================
# 3. Build scatterplot
# =============================================================================

def build_scatter(x_col, y_col, color_by):
    ib_df = _state['ib_df']

    clear_output(wait=True)
    print("="*60)
    print(f"SCATTERPLOT: {y_col} vs {x_col}")
    print("="*60)

    fig, ax = plt.subplots(figsize=(9, 7))

    if color_by == 'None':
        ax.scatter(ib_df[x_col], ib_df[y_col], alpha=0.5, s=40, color='#003366', edgecolor='white', linewidth=0.5)
        ax.set_title(f'{y_col} vs {x_col}', fontsize=13, color='#003366')
    elif color_by == 'Cluster':
        clusters = sorted(ib_df['Cluster'].unique())
        colors = ['#E37222', '#003366', '#64748b', '#22c55e', '#a855f7'][:len(clusters)]
        for cl, col in zip(clusters, colors):
            subset = ib_df[ib_df['Cluster'] == cl]
            ax.scatter(subset[x_col], subset[y_col], alpha=0.6, s=50, 
                       color=col, edgecolor='white', linewidth=0.5, label=f'Cluster {cl}')
        ax.legend(title='Cluster', loc='best')
        ax.set_title(f'{y_col} vs {x_col} (colored by Cluster)', fontsize=13, color='#003366')
    elif color_by == 'Segment (True)':
        segments = sorted(ib_df['Segment'].unique())
        colors = ['#E37222', '#003366', '#64748b', '#22c55e', '#a855f7'][:len(segments)]
        for seg, col in zip(segments, colors):
            subset = ib_df[ib_df['Segment'] == seg]
            ax.scatter(subset[x_col], subset[y_col], alpha=0.6, s=50, 
                       color=col, edgecolor='white', linewidth=0.5, label=seg)
        ax.legend(title='True Segment', loc='best')
        ax.set_title(f'{y_col} vs {x_col} (colored by True Segment)', fontsize=13, color='#003366')

    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--')
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--')
    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    plt.tight_layout()
    plt.show()

    # Correlation
    corr = ib_df[x_col].corr(ib_df[y_col])
    print(f"\nPearson correlation: r = {corr:.3f}")
    if abs(corr) > 0.5:
        print("   → Strong linear relationship: these preferences move together")
    elif abs(corr) > 0.2:
        print("   → Moderate relationship: some respondents want both, others trade off")
    else:
        print("   → Weak or no relationship: these preferences are largely independent")

    # Show controls again for iteration
    print("\n" + "-"*60)
    print("Try another combination:")
    print("-"*60)
    show_controls()

if proceed:
    show_controls()
