# ═══════════════════════════════════════════════════════════════════
#  STEP 2: Generic Metric Conjoint Analysis Tool (MVP)
# ═══════════════════════════════════════════════════════════════════

import io
import numpy as np
import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from sklearn.linear_model import LinearRegression

# =============================================================================
# STATE
# =============================================================================

df = None          # uploaded data
resp_col = None    # respondent ID column
task_col = None    # task/profile ID column
y_col = None       # rating/choice column
x_cols = []        # attribute columns
dummies = None     # dataframe with dummy variables
ib_df = None       # individual betas
agg_model = None   # aggregate OLS model

# =============================================================================
# PANELS
# =============================================================================

out_upload = widgets.Output()
out_mapping = widgets.Output()
out_analysis = widgets.Output()
out_viz = widgets.Output()

# =============================================================================
# PHASE 1: UPLOAD
# =============================================================================

upload_widget = widgets.FileUpload(
    accept='.csv', multiple=False, description='📁 Upload CSV',
    button_style='primary', layout=widgets.Layout(width='300px'))

btn_load = widgets.Button(description='▶ Load CSV', button_style='success')

def on_load(_):
    global df
    with out_upload:
        clear_output()
        if not upload_widget.value:
            print("❌ Select a CSV file first."); return
        
        raw = list(upload_widget.value.values())[0]['content']
        df = pd.read_csv(io.BytesIO(raw))
        
        print(f"✅ Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Numeric: {[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]}")
        print(f"   Categorical: {[c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]}")
        print("\n   First 5 rows:")
        display(df.head())
        
        # Auto-detect candidates
        build_mapping_ui()

btn_load.on_click(on_load)

upload_ui = widgets.VBox([
    widgets.HTML("<h2>Metric Conjoint Tool: Step 1 — Upload</h2>"),
    widgets.HTML("<p>Upload your conjoint data CSV. Must contain respondent IDs, task/profile IDs, a rating/choice column, and attribute columns.</p>"),
    widgets.HBox([upload_widget, btn_load]),
    out_upload
])

# =============================================================================
# PHASE 2: COLUMN MAPPING
# =============================================================================

dd_resp = widgets.Dropdown(options=[], description='Resp ID:', layout=widgets.Layout(width='280px'))
dd_task = widgets.Dropdown(options=[], description='Task ID:', layout=widgets.Layout(width='280px'))
dd_y = widgets.Dropdown(options=[], description='Y (rating):', layout=widgets.Layout(width='280px'))
sel_x = widgets.SelectMultiple(options=[], description='X (attrs):', rows=6, layout=widgets.Layout(width='300px', height='180px'))

btn_map = widgets.Button(description='▶ Confirm Mapping', button_style='success')
btn_auto = widgets.Button(description='💡 Auto-Detect', button_style='info')

def build_mapping_ui():
    with out_mapping:
        clear_output()
        
        all_cols = list(df.columns)
        numeric_cols = [c for c in all_cols if pd.api.types.is_numeric_dtype(df[c])]
        cat_cols = [c for c in all_cols if c not in numeric_cols]
        
        # Update dropdowns
        dd_resp.options = all_cols
        dd_task.options = all_cols
        dd_y.options = numeric_cols
        sel_x.options = all_cols
        
        # Auto-guess
        resp_guess = next((c for c in all_cols if 'resp' in c.lower() or 'id' in c.lower()), all_cols[0])
        task_guess = next((c for c in all_cols if 'task' in c.lower() or 'profile' in c.lower() or 'trial' in c.lower()), all_cols[1] if len(all_cols) > 1 else all_cols[0])
        y_guess = next((c for c in numeric_cols if 'rating' in c.lower() or 'choice' in c.lower() or 'score' in c.lower() or 'y' in c.lower()), numeric_cols[0] if numeric_cols else None)
        
        dd_resp.value = resp_guess
        dd_task.value = task_guess
        if y_guess:
            dd_y.value = y_guess
        
        # Auto-guess X: all non-ID, non-Y columns
        auto_x = [c for c in all_cols if c not in [resp_guess, task_guess, y_guess]]
        sel_x.value = tuple(auto_x)
        
        display(widgets.HTML("<h3>Step 2 — Map Columns</h3>"))
        display(widgets.HBox([dd_resp, dd_task, dd_y]))
        display(sel_x)
        display(widgets.HBox([btn_auto, btn_map]))

def on_auto(_):
    build_mapping_ui()

def on_map(_):
    global resp_col, task_col, y_col, x_cols
    
    resp_col = dd_resp.value
    task_col = dd_task.value
    y_col = dd_y.value
    x_cols = list(sel_x.value)
    
    with out_mapping:
        clear_output()
        print("="*60)
        print("COLUMN MAPPING CONFIRMED")
        print("="*60)
        print(f"  Respondent ID : {resp_col}")
        print(f"  Task/Profile  : {task_col}")
        print(f"  Y variable    : {y_col}")
        print(f"  X attributes  : {x_cols}")
        
        # Validate
        n_resp = df[resp_col].nunique()
        n_tasks = df[task_col].nunique()
        print(f"\n  Respondents   : {n_resp}")
        print(f"  Tasks/profiles: {n_tasks}")
        print(f"  Rows per resp : {len(df) / n_resp:.1f}")
        
        if len(x_cols) == 0:
            print("\n❌ Select at least one X attribute.")
            return
        
        print("\n✅ Mapping locked. Run analysis next.")

btn_auto.on_click(on_auto)
btn_map.on_click(on_map)

# =============================================================================
# PHASE 3: RUN ANALYSIS
# =============================================================================

btn_run = widgets.Button(description='▶ Run Analysis', button_style='success', layout=widgets.Layout(width='200px'))

def make_dummies(df_in, cols, resp_id_col):
    """Create dummy variables for selected categorical columns."""
    out = df_in.copy()
    dummy_cols = []
    
    for col in cols:
        unique_vals = sorted(df_in[col].dropna().unique())
        if len(unique_vals) < 2:
            continue  # Skip single-level attributes
        
        # Use first value as reference
        ref = unique_vals[0]
        for val in unique_vals[1:]:
            dummy_name = f"d_{col}_{str(val).replace(' ', '_')}"
            out[dummy_name] = (df_in[col] == val).astype(int)
            dummy_cols.append(dummy_name)
        
        print(f"  {col}: reference = '{ref}', dummies = {len(unique_vals)-1}")
    
    return out, dummy_cols

def compute_importance(row, attr_map):
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

def on_run(_):
    global dummies, ib_df, agg_model
    
    with out_analysis:
        clear_output()
        
        if resp_col is None or y_col is None or len(x_cols) == 0:
            print("❌ Complete Step 2 (column mapping) first.")
            return
        
        print("="*60)
        print("RUNNING METRIC CONJOINT ANALYSIS")
        print("="*60)
        
        # Step 3a: Create dummies
        print("\n--- Creating Dummy Variables ---")
        dummies, dummy_cols = make_dummies(df, x_cols, resp_col)
        
        if len(dummy_cols) == 0:
            print("❌ No valid dummy variables created. Check X attributes.")
            return
        
        # Build attr_map
        attr_map = {}
        for col in x_cols:
            attr_map[col] = [d for d in dummy_cols if d.startswith(f"d_{col}_")]
        
        print(f"\nTotal dummy variables: {len(dummy_cols)}")
        
        # Step 3b: Aggregate OLS
        print("\n--- Aggregate OLS ---")
        X = dummies[dummy_cols].values
        y = dummies[y_col].values
        
        agg_model = LinearRegression()
        agg_model.fit(X, y)
        
        print(f"Intercept: {agg_model.intercept_:.3f}")
        print("\nPart-worths (vs reference level):")
        for col, coef in zip(dummy_cols, agg_model.coef_):
            print(f"  {col:30s}: {coef:7.3f}")
        
        # Aggregate importance
        agg_pws = {'Intercept': agg_model.intercept_}
        for d, c in zip(dummy_cols, agg_model.coef_):
            agg_pws[d] = c
        
        imp = {}
        for attr, dummies_list in attr_map.items():
            pws = [agg_pws.get(d, 0) for d in dummies_list]
            imp[attr] = max(pws) - min(pws)
        total_imp = sum(imp.values())
        
        print("\nAttribute Importance (%):")
        for attr, val in sorted(imp.items(), key=lambda x: -x[1]):
            print(f"  {attr:20s}: {val/total_imp*100:5.1f}%")
        
        # Step 3c: Individual-level OLS
        print("\n--- Individual-Level Models ---")
        individual_betas = []
        n_estimated = 0
        n_skipped = 0
        
        for resp_id in dummies[resp_col].unique():
            resp_data = dummies[dummies[resp_col] == resp_id].copy()
            Xi = resp_data[dummy_cols].values
            yi = resp_data[y_col].values
            
            if len(yi) < 2 or np.any(Xi.std(axis=0) == 0):
                n_skipped += 1
                continue
            
            mi = LinearRegression()
            mi.fit(Xi, yi)
            
            row = {resp_col: resp_id}
            for d, c in zip(dummy_cols, mi.coef_):
                row[d] = c
            row['Intercept'] = mi.intercept_
            individual_betas.append(row)
            n_estimated += 1
        
        ib_df = pd.DataFrame(individual_betas)
        print(f"Estimated: {n_estimated} individual models")
        print(f"Skipped  : {n_skipped} (insufficient variation)")
        
        # Compute importance per person
        imp_records = []
        for _, row in ib_df.iterrows():
            imp = compute_importance(row, attr_map)
            imp_records.append(imp)
        
        imp_df = pd.DataFrame(imp_records)
        imp_df[resp_col] = ib_df[resp_col].values
        
        print("\nMean importance across respondents:")
        print(imp_df.drop(resp_col, axis=1).mean().round(1).sort_values(ascending=False))
        
        # Store in globals for viz
        import builtins
        builtins.ib_df = ib_df
        builtins.imp_df = imp_df
        builtins.attr_map = attr_map
        builtins.dummy_cols = dummy_cols
        builtins.metric_tool_attr_map = attr_map
        builtins.metric_tool_dummy_cols = dummy_cols
        builtins.metric_tool_resp_col = resp_col
        
        print("\n✅ Analysis complete. Visualizations below.")
    
    # Render viz
    with out_viz:
        clear_output()
        render_visualizations(ib_df, imp_df, attr_map, dummy_cols, resp_col)

btn_run.on_click(on_run)

# =============================================================================
# PHASE 4: VISUALIZATIONS
# =============================================================================

def render_visualizations(ib_df, imp_df, attr_map, dummy_cols, resp_col):
    """Create adaptive 2×2 visualization grid from any conjoint data."""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    
    # ── Plot 1: Boxplot of top part-worths ──
    ax = axes[0, 0]
    
    # Top 4 attributes by mean importance
    mean_imp = imp_df.drop(resp_col, axis=1).mean().sort_values(ascending=False)
    top4_attrs = list(mean_imp.index[:min(4, len(mean_imp))])
    
    box_data = []
    box_labels = []
    for attr in top4_attrs:
        dummies_list = attr_map.get(attr, [])
        for d in dummies_list[:2]:  # Max 2 dummies per attr to avoid clutter
            if d in ib_df.columns:
                vals = ib_df[d].dropna().values
                if len(vals) > 0:
                    box_data.append(vals)
                    box_labels.append(d.replace('d_', '').replace('_', ' ')[:20])
    
    if box_data:
        bp = ax.boxplot(box_data, labels=box_labels, patch_artist=True)
        colors = ['#2c7a7b', '#718096', '#d69e2e', '#e53e3e', '#805ad5', '#dd6b20']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        ax.set_ylabel('Part-Worth')
        ax.set_title('Dispersion of Individual Part-Worths')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    else:
        ax.text(0.5, 0.5, 'No valid part-worths to plot', ha='center', va='center', transform=ax.transAxes)
    
    # ── Plot 2: Scatter of top 2 part-worths ──
    ax = axes[0, 1]
    
    all_dummies = [d for dummies_list in attr_map.values() for d in dummies_list if d in ib_df.columns]
    if len(all_dummies) >= 2:
        dummy_means = [(d, ib_df[d].abs().mean()) for d in all_dummies]
        dummy_means.sort(key=lambda x: -x[1])
        d1, d2 = dummy_means[0][0], dummy_means[1][0]
        
        # Check for segment column
        seg_col = None
        for c in ['Segment', 'segment', 'Cluster', 'cluster', 'Group', 'group']:
            if c in df.columns:
                seg_col = c
                break
        
        if seg_col:
            seg_map = df.groupby(resp_col)[seg_col].first().to_dict()
            ib_df['_seg'] = ib_df[resp_col].map(seg_map)
            segments = ib_df['_seg'].dropna().unique()
            colors = ['#2c7a7b', '#d69e2e', '#e53e3e', '#805ad5', '#dd6b20']
            for i, seg in enumerate(segments[:5]):
                mask = ib_df['_seg'] == seg
                ax.scatter(ib_df.loc[mask, d1], ib_df.loc[mask, d2],
                          alpha=0.4, s=25, c=colors[i % len(colors)], label=str(seg))
            ax.legend(title=seg_col, loc='best')
        else:
            ax.scatter(ib_df[d1], ib_df[d2], alpha=0.4, s=25, c='#718096')
        
        ax.set_xlabel(f"{d1.replace('d_', '').replace('_', ' ')[:25]}")
        ax.set_ylabel(f"{d2.replace('d_', '').replace('_', ' ')[:25]}")
        ax.set_title('Preference Landscape: Top 2 Part-Worths')
        ax.axhline(0, color='gray', linestyle='--', alpha=0.3)
        ax.axvline(0, color='gray', linestyle='--', alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'Need ≥2 dummy variables', ha='center', va='center', transform=ax.transAxes)
    
    # ── Plot 3: Attribute importance by segment ──
    ax = axes[1, 0]
    
    if seg_col and len(top4_attrs) > 0:
        imp_df['_seg'] = imp_df[resp_col].map(seg_map)
        seg_imp = imp_df.groupby('_seg')[top4_attrs].mean()
        
        x = np.arange(len(top4_attrs))
        w = 0.8 / len(seg_imp)
        
        for i, (seg, color) in enumerate(zip(seg_imp.index, colors)):
            ax.bar(x + i*w, seg_imp.loc[seg], w, label=str(seg), color=color, edgecolor='black')
        
        ax.set_xticks(x + w * (len(seg_imp)-1) / 2)
        ax.set_xticklabels(top4_attrs, rotation=15, ha='right')
        ax.set_ylabel('Importance (%)')
        ax.set_title('Attribute Importance by Segment')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'No segment labels found', ha='center', va='center', transform=ax.transAxes)
    
    # ── Plot 4: Chasm map (price vs. tech, if available) ──
    ax = axes[1, 1]
    
    # Auto-detect price and tech columns
    price_cols = [d for d in dummy_cols if any(k in d.lower() for k in ['price', 'cost'])]
    tech_cols = [d for d in dummy_cols if any(k in d.lower() for k in ['smart', 'tech', 'feature', 'advanced'])]
    
    if price_cols and tech_cols and seg_col:
        ib_df['Price_Sensitivity'] = ib_df[price_cols].max(axis=1) - ib_df[price_cols].min(axis=1)
        ib_df['Tech_Appetite'] = ib_df[tech_cols].mean(axis=1)
        
        for seg, color in zip(ib_df['_seg'].unique(), colors):
            mask = ib_df['_seg'] == seg
            ax.scatter(ib_df.loc[mask, 'Price_Sensitivity'], ib_df.loc[mask, 'Tech_Appetite'],
                      alpha=0.4, s=30, c=color, label=str(seg))
        
        ax.set_xlabel('Price Sensitivity (range of price part-worths)')
        ax.set_ylabel('Tech/Feature Appetite')
        ax.set_title('The Chasm Map')
        ax.legend(title=seg_col)
        ax.axhline(0, color='gray', linestyle='--', alpha=0.3)
        ax.axvline(0, color='gray', linestyle='--', alpha=0.3)
    else:
        # Fallback: show correlation matrix of top attributes
        if len(top4_attrs) >= 2:
            corr_data = imp_df[top4_attrs].corr()
            im = ax.imshow(corr_data, cmap='RdBu_r', vmin=-1, vmax=1)
            ax.set_xticks(range(len(top4_attrs)))
            ax.set_yticks(range(len(top4_attrs)))
            ax.set_xticklabels(top4_attrs, rotation=45, ha='right')
            ax.set_yticklabels(top4_attrs)
            ax.set_title('Attribute Importance Correlations')
            plt.colorbar(im, ax=ax)
        else:
            ax.text(0.5, 0.5, 'Need price + tech attributes\nfor chasm map', ha='center', va='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.show()
    
    # ── Socratic questions ──
    print("\n" + "="*60)
    print("DISCUSSION QUESTIONS")
    print("="*60)
    print(f"""
1. DISPERSION: Which attribute has the widest spread in part-worths?
   → Wide spread = people disagree. That is your segmentation opportunity.

2. TRIBES: Look at the scatter plot. Are there distinct clouds of points?
   → If yes, you have found preference tribes.

3. SEGMENTS: Do the segment bars diverge on any attribute?
   → Where they diverge = where the chasm lives.

4. YOUR PRODUCT: Where would you place your current product on the chasm map?
   Where would you place a product for the pragmatist beachhead?
    """)

# =============================================================================
# ASSEMBLE FULL UI
# =============================================================================

analysis_ui = widgets.VBox([
    widgets.HTML("<h3>Step 3 — Run Analysis</h3>"),
    btn_run,
    out_analysis
])

viz_ui = widgets.VBox([
    out_viz
])

full_ui = widgets.VBox([
    widgets.HTML("<h2>Generic Metric Conjoint Analysis Tool</h2>"),
    upload_ui,
    widgets.HTML("<hr>"),
    out_mapping,
    widgets.HTML("<hr>"),
    analysis_ui,
    widgets.HTML("<hr>"),
    viz_ui
])

display(full_ui)
