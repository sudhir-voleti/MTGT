# ═══════════════════════════════════════════════════════════════════
#  STEP 2: Metric Conjoint — Preference Discovery Lab
# ═══════════════════════════════════════════════════════════════════

import io
import numpy as np
import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from sklearn.linear_model import LinearRegression

# ── Guard: Step 1 must have run ──
try:
    metric_df
except NameError:
    raise RuntimeError("Run Step 1 first! Upload the CSV files.")

# =============================================================================
# PANEL A: What Do You Want to Model?
# =============================================================================

# Auto-detect columns from uploaded data
all_cols = list(metric_df.columns)
numeric_cols = [c for c in all_cols if pd.api.types.is_numeric_dtype(metric_df[c])]
categorical_cols = [c for c in all_cols if c not in numeric_cols and c not in ['RespID', 'ProfileID', 'Segment']]

out_theory = widgets.Output()
out_controls = widgets.Output()
out_results = widgets.Output()
out_viz = widgets.Output()

# ── Theory intro (collapsible, but visible by default) ──
with out_theory:
    print("=" * 60)
    print("THEORY: What is a Part-Worth?")
    print("=" * 60)
    print("""
Every respondent saw 16 product profiles and rated each one.
Those ratings are a weighted sum of how much they like each attribute level.

Example: A respondent who loves range and hates price might have:
  150km range  →  +3.2 points to their rating
  140K price   →  -2.1 points to their rating

Your job: Run one regression per respondent to recover these weights.
Then look at the distribution across all 400 people.
    """)

# ── Control panel ──
dd_y = widgets.Dropdown(
    options=[c for c in numeric_cols if c not in ['RespID', 'ProfileID']],
    value='Rating' if 'Rating' in numeric_cols else numeric_cols[0],
    description='Y (rating):',
    layout=widgets.Layout(width='280px'))

# Multi-select for X variables (attributes)
# Auto-suggest: all categorical columns except IDs
default_x = [c for c in categorical_cols if c not in ['RespID', 'ProfileID', 'Segment']]
sel_x = widgets.SelectMultiple(
    options=categorical_cols,
    value=tuple(default_x),
    description='X (attributes):',
    rows=6,
    layout=widgets.Layout(width='300px', height='180px'))

btn_run = widgets.Button(description='▶ Run Preference Discovery', button_style='success')
btn_reset = widgets.Button(description='🗑 Reset', button_style='warning')

status_html = widgets.HTML("<i>Select Y and X, then run.</i>")

controls = widgets.VBox([
    widgets.HTML("<h3>Build Your Model</h3>"),
    widgets.HBox([dd_y, sel_x]),
    widgets.HBox([btn_run, btn_reset]),
    status_html
])

with out_controls:
    display(controls)

# =============================================================================
# PANEL B: Results (hidden until run)
# =============================================================================

# =============================================================================
# PANEL C: Visualizations (hidden until run)
# =============================================================================

# =============================================================================
# HELPERS
# =============================================================================

def make_dummies(df, cols):
    """Create dummy variables for selected categorical columns."""
    dummies = df.copy()
    dummy_cols = []
    
    for col in cols:
        unique_vals = sorted(df[col].dropna().unique())
        # Skip first as reference
        for val in unique_vals[1:]:
            dummy_name = f"d_{col}_{val}"
            dummies[dummy_name] = (df[col] == val).astype(int)
            dummy_cols.append(dummy_name)
    
    return dummies, dummy_cols

def compute_importance(row, dummy_cols, attr_map):
    """Compute attribute importance from part-worths."""
    importance = {}
    for attr, dummies in attr_map.items():
        pws = [row.get(d, 0) for d in dummies]
        if len(pws) > 0:
            importance[attr] = max(pws) - min(pws)
    total = sum(importance.values())
    if total == 0:
        return {k: 0 for k in importance}
    return {k: v/total*100 for k, v in importance.items()}

# =============================================================================
# EVENT HANDLERS
# =============================================================================

individual_betas = None
ib_df = None
attr_map = {}

def on_run(_):
    global individual_betas, ib_df, attr_map
    
    with out_results:
        clear_output()
        
        y_col = dd_y.value
        x_cols = list(sel_x.value)
        
        if not x_cols:
            print("❌ Select at least one X variable."); return
        
        print(f"Y = {y_col}")
        print(f"X = {', '.join(x_cols)}")
        print("\n" + "="*60)
        print("STEP 1: Aggregate OLS (What does the average person want?)")
        print("="*60)
        
        # Make dummies
        dummies, dummy_cols = make_dummies(metric_df, x_cols)
        attr_map = {}
        for col in x_cols:
            attr_map[col] = [d for d in dummy_cols if d.startswith(f"d_{col}_")]
        
        X = dummies[dummy_cols].values
        y = dummies[y_col].values
        
        agg_model = LinearRegression()
        agg_model.fit(X, y)
        
        print(f"Intercept (baseline rating): {agg_model.intercept_:.3f}")
        print("\nPart-worths (vs reference level):")
        for col, coef in zip(dummy_cols, agg_model.coef_):
            print(f"  {col:25s}: {coef:7.3f}")
        
        # Attribute importance
        agg_pws = {'Intercept': agg_model.intercept_}
        for d, c in zip(dummy_cols, agg_model.coef_):
            agg_pws[d] = c
        
        imp = {}
        for attr, dummies in attr_map.items():
            pws = [agg_pws.get(d, 0) for d in dummies]
            imp[attr] = max(pws) - min(pws)
        total_imp = sum(imp.values())
        
        print("\nAttribute Importance (%):")
        for attr, val in sorted(imp.items(), key=lambda x: -x[1]):
            print(f"  {attr:15s}: {val/total_imp*100:5.1f}%")
        
        # ── Individual-level models ──
        print("\n" + "="*60)
        print("STEP 2: Individual Models (400 regressions, one per person)")
        print("="*60)
        
        individual_betas = []
        n_estimated = 0
        
        for resp_id in metric_df['RespID'].unique():
            resp_data = dummies[dummies['RespID'] == resp_id].copy()
            Xi = resp_data[dummy_cols].values
            yi = resp_data[y_col].values
            
            if np.any(Xi.std(axis=0) == 0):
                continue
            
            mi = LinearRegression()
            mi.fit(Xi, yi)
            
            row = {'RespID': resp_id}
            for d, c in zip(dummy_cols, mi.coef_):
                row[d] = c
            row['Intercept'] = mi.intercept_
            individual_betas.append(row)
            n_estimated += 1
        
        ib_df = pd.DataFrame(individual_betas)
        print(f"Estimated: {n_estimated} individual models")
        
        # Compute importance per person
        imp_records = []
        for _, row in ib_df.iterrows():
            imp = compute_importance(row, dummy_cols, attr_map)
            imp_records.append(imp)
        
        imp_df = pd.DataFrame(imp_records)
        imp_df['RespID'] = ib_df['RespID'].values
        
        print("\nMean importance across all respondents:")
        print(imp_df.drop('RespID', axis=1).mean().round(1).sort_values(ascending=False))
        
        # Store for viz
        import builtins
        builtins.ib_df = ib_df
        builtins.imp_df = imp_df
        builtins.attr_map = attr_map
        builtins.dummy_cols = dummy_cols
        
        print("\n✅ Models stored. Visualizations below.")
    
    # ── Render visualizations ──
    with out_viz:
        clear_output()
        render_visualizations(ib_df, imp_df, attr_map, dummy_cols)

def render_visualizations(ib_df, imp_df, attr_map, dummy_cols):
    """Create the 2×2 visualization grid."""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    
    # ── Plot 1: Boxplot of individual part-worths (top 4 attributes) ──
    ax = axes[0, 0]
    
    # Pick top 4 attributes by mean importance
    mean_imp = imp_df.drop('RespID', axis=1).mean().sort_values(ascending=False)
    top4_attrs = list(mean_imp.index[:4])
    
    box_data = []
    box_labels = []
    for attr in top4_attrs:
        dummies = attr_map.get(attr, [])
        for d in dummies:
            if d in ib_df.columns:
                box_data.append(ib_df[d].dropna().values)
                box_labels.append(d.replace('d_', '').replace('_', ' '))
    
    if box_data:
        bp = ax.boxplot(box_data, labels=box_labels, patch_artist=True)
        colors = ['#2c7a7b', '#718096', '#d69e2e', '#e53e3e'] * 3
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        ax.set_ylabel('Part-Worth')
        ax.set_title('Dispersion of Individual Part-Worths\n(Each dot = one person\'s preference weight)')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    
    # ── Plot 2: Scatter of top 2 part-worths ──
    ax = axes[0, 1]
    
    # Top 2 most important dummies
    all_dummies = [d for dummies in attr_map.values() for d in dummies if d in ib_df.columns]
    dummy_means = [(d, ib_df[d].abs().mean()) for d in all_dummies]
    dummy_means.sort(key=lambda x: -x[1])
    
    if len(dummy_means) >= 2:
        d1, d2 = dummy_means[0][0], dummy_means[1][0]
        
        # Color by segment if available
        if 'Segment' in metric_df.columns:
            seg_colors = {'Tech': '#2c7a7b', 'Pragmatist': '#d69e2e', 'PriceHunter': '#e53e3e'}
            for seg in metric_df['Segment'].unique():
                resp_ids = metric_df[metric_df['Segment'] == seg]['RespID'].unique()
                mask = ib_df['RespID'].isin(resp_ids)
                ax.scatter(ib_df.loc[mask, d1], ib_df.loc[mask, d2],
                          alpha=0.4, s=25, c=seg_colors.get(seg, '#718096'), label=seg)
            ax.legend(title='True Segment', loc='best')
        else:
            ax.scatter(ib_df[d1], ib_df[d2], alpha=0.4, s=25, c='#718096')
        
        ax.set_xlabel(f"{d1.replace('d_', '').replace('_', ' ')} part-worth")
        ax.set_ylabel(f"{d2.replace('d_', '').replace('_', ' ')} part-worth")
        ax.set_title('Preference Landscape: Top 2 Part-Worths\n(Each point = one respondent)')
        ax.axhline(0, color='gray', linestyle='--', alpha=0.3)
        ax.axvline(0, color='gray', linestyle='--', alpha=0.3)
    
    # ── Plot 3: Attribute importance by segment (if segment known) ──
    ax = axes[1, 0]
    
    if 'Segment' in metric_df.columns:
        # Merge segment labels
        seg_map = metric_df.groupby('RespID')['Segment'].first().to_dict()
        imp_df['Segment'] = imp_df['RespID'].map(seg_map)
        
        seg_imp = imp_df.groupby('Segment')[top4_attrs].mean()
        x = np.arange(len(top4_attrs))
        w = 0.25
        
        for i, (seg, color) in enumerate(zip(seg_imp.index, ['#2c7a7b', '#d69e2e', '#e53e3e'])):
            ax.bar(x + i*w, seg_imp.loc[seg], w, label=seg, color=color, edgecolor='black')
        
        ax.set_xticks(x + w)
        ax.set_xticklabels(top4_attrs, rotation=15, ha='right')
        ax.set_ylabel('Importance (%)')
        ax.set_title('Attribute Importance by Segment\n(Do early adopters and pragmatists want different things?)')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'No segment labels in data', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Segment comparison unavailable')
    
    # ── Plot 4: The "Socratic" plot — Where is the chasm? ──
    ax = axes[1, 1]
    
    # Plot: Price sensitivity vs. Smart feature preference
    # These two usually diverge across segments
    price_cols = [d for d in dummy_cols if 'Price' in d]
    smart_cols = [d for d in dummy_cols if 'Smart' in d]
    
    if price_cols and smart_cols and 'Segment' in metric_df.columns:
        # Compute per-person price sensitivity (max price PW) and smart preference
        ib_df['Price_Sensitivity'] = ib_df[price_cols].max(axis=1) - ib_df[price_cols].min(axis=1)
        ib_df['Smart_Preference'] = ib_df[smart_cols].mean(axis=1)
        ib_df['Segment'] = ib_df['RespID'].map(seg_map)
        
        for seg, color in zip(ib_df['Segment'].unique(), ['#2c7a7b', '#d69e2e', '#e53e3e']):
            mask = ib_df['Segment'] == seg
            ax.scatter(ib_df.loc[mask, 'Price_Sensitivity'], ib_df.loc[mask, 'Smart_Preference'],
                      alpha=0.4, s=30, c=color, label=seg)
        
        ax.set_xlabel('Price Sensitivity (range of price part-worths)')
        ax.set_ylabel('Smart Feature Preference')
        ax.set_title('The Chasm Map: Price vs. Tech Appetite\n(Where do your segments sit?)')
        ax.legend(title='Segment')
        ax.axhline(0, color='gray', linestyle='--', alpha=0.3)
        ax.axvline(0, color='gray', linestyle='--', alpha=0.3)
        
        # Quadrant labels
        ax.text(0.95, 0.95, 'Price Hunters\n(Low tech, high price sensitivity)', 
               transform=ax.transAxes, ha='right', va='top', fontsize=9, 
               bbox=dict(boxstyle='round', facecolor='#fff5f5', edgecolor='#e53e3e'))
        ax.text(0.05, 0.95, 'Tech Enthusiasts\n(High tech, low price sensitivity)', 
               transform=ax.transAxes, ha='left', va='top', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='#e6fffa', edgecolor='#2c7a7b'))
    else:
        ax.text(0.5, 0.5, 'Chasm map requires Price and Smart attributes', 
               ha='center', va='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.show()
    
    # ── Socratic questions ──
    print("\n" + "="*60)
    print("SOCRATIC QUESTIONS")
    print("="*60)
    print("""
1. Look at the boxplot (top-left). Which attribute has the widest dispersion?
   → Wide dispersion = people disagree. That is your segmentation opportunity.

2. Look at the scatter (top-right). Are there distinct clouds of points?
   → If yes, you have found tribes. If no, the market is homogeneous.

3. Look at the segment bars (bottom-left). Which attribute most separates
   the segments? → That is where the chasm lives.

4. Look at the chasm map (bottom-right). Where would you place the S1?
   Where would you place a Pragmatist SKU?
    """)

def on_reset(_):
    with out_results:
        clear_output()
    with out_viz:
        clear_output()
    status_html.value = "<i>Select Y and X, then run.</i>"

btn_run.on_click(on_run)
btn_reset.on_click(on_reset)

# =============================================================================
# ASSEMBLE UI
# =============================================================================

ui = widgets.VBox([
    widgets.HTML("<h2>Step 2: Preference Discovery Lab</h2>"),
    out_theory,
    out_controls,
    out_results,
    out_viz
])

display(ui)
