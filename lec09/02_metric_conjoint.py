# ═══════════════════════════════════════════════════════════════════
#  STEP 2: Generic Metric Conjoint Analysis Tool (MVP) — FIXED
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

df = None
mapping_locked = False
resp_col = None
task_col = None
y_col = None
x_cols = []
seg_col = None  # optional

dummies = None
ib_df = None
agg_model = None
attr_map = {}

# =============================================================================
# OUTPUT AREAS
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
        
        build_mapping_ui()

btn_load.on_click(on_load)

upload_ui = widgets.VBox([
    widgets.HTML("<h2>Metric Conjoint Tool: Step 1 — Upload</h2>"),
    widgets.HTML("<p>Upload your conjoint data CSV. Required columns: respondent ID, task/profile ID, rating/choice (Y), and at least one attribute.</p>"),
    widgets.HBox([upload_widget, btn_load]),
    out_upload
])

# =============================================================================
# PHASE 2: COLUMN MAPPING (with lock)
# =============================================================================

dd_resp = widgets.Dropdown(options=[], description='Resp ID*:', layout=widgets.Layout(width='260px'))
dd_task = widgets.Dropdown(options=[], description='Task ID*:', layout=widgets.Layout(width='260px'))
dd_y = widgets.Dropdown(options=[], description='Y (rating)*:', layout=widgets.Layout(width='260px'))
dd_seg = widgets.Dropdown(options=['-- None --'], description='Segment:', layout=widgets.Layout(width='260px'))
sel_x = widgets.SelectMultiple(options=[], description='Attributes*:', rows=6, layout=widgets.Layout(width='300px', height='200px'))

btn_auto = widgets.Button(description='💡 Auto-Detect', button_style='info')
btn_lock = widgets.Button(description='🔒 Lock Mapping', button_style='success', disabled=True)
btn_reset = widgets.Button(description='🗑 Reset', button_style='warning')

status_html = widgets.HTML("<i>Select mandatory fields (*), then lock.</i>")

def build_mapping_ui():
    with out_mapping:
        clear_output()
        
        all_cols = list(df.columns)
        numeric_cols = [c for c in all_cols if pd.api.types.is_numeric_dtype(df[c])]
        cat_cols = [c for c in all_cols if c not in numeric_cols]
        
        dd_resp.options = all_cols
        dd_task.options = all_cols
        dd_y.options = numeric_cols
        dd_seg.options = ['-- None --'] + all_cols
        sel_x.options = all_cols
        
        # Auto-guess
        resp_guess = next((c for c in all_cols if any(k in c.lower() for k in ['resp', 'id', 'subject', 'panelist'])), all_cols[0])
        task_guess = next((c for c in all_cols if any(k in c.lower() for k in ['task', 'profile', 'trial', 'concept', 'card'])), all_cols[1] if len(all_cols) > 1 else all_cols[0])
        y_guess = next((c for c in numeric_cols if any(k in c.lower() for k in ['rating', 'choice', 'score', 'y', 'preference', 'liking'])), numeric_cols[0] if numeric_cols else None)
        seg_guess = next((c for c in all_cols if any(k in c.lower() for k in ['segment', 'cluster', 'group', 'seg'])), '-- None --')
        
        dd_resp.value = resp_guess
        dd_task.value = task_guess
        if y_guess:
            dd_y.value = y_guess
        dd_seg.value = seg_guess if seg_guess in dd_seg.options else '-- None --'
        
        # Auto-guess X: exclude ID, Y, segment columns
        exclude = {resp_guess, task_guess, y_guess, seg_guess} if seg_guess != '-- None --' else {resp_guess, task_guess, y_guess}
        auto_x = [c for c in all_cols if c not in exclude and c not in ['-- None --']]
        sel_x.value = tuple(auto_x)
        
        # Enable lock button
        btn_lock.disabled = False
        
        display(widgets.HTML("<h3>Step 2 — Map Columns</h3>"))
        display(widgets.HTML("<p><b>Required (*):</b> Respondent ID, Task/Profile ID, Y variable, at least one X attribute.<br><b>Optional:</b> Segment label for validation.</p>"))
        display(widgets.HBox([dd_resp, dd_task, dd_y, dd_seg]))
        display(sel_x)
        display(widgets.HBox([btn_auto, btn_lock, btn_reset]))
        display(status_html)

def on_auto(_):
    build_mapping_ui()

def check_mandatory():
    """Return error message if any mandatory field missing, else None."""
    if dd_resp.value is None or dd_resp.value == '':
        return "Select Respondent ID"
    if dd_task.value is None or dd_task.value == '':
        return "Select Task/Profile ID"
    if dd_y.value is None or dd_y.value == '':
        return "Select Y variable (rating/choice)"
    if len(sel_x.value) == 0:
        return "Select at least one X attribute"
    if dd_resp.value == dd_task.value:
        return "Resp ID and Task ID must be different columns"
    if dd_y.value in sel_x.value:
        return "Y variable cannot also be an X attribute"
    return None

def on_lock(_):
    global mapping_locked, resp_col, task_col, y_col, x_cols, seg_col
    
    err = check_mandatory()
    if err:
        status_html.value = f"<span style='color:#c53030'>❌ {err}</span>"
        return
    
    resp_col = dd_resp.value
    task_col = dd_task.value
    y_col = dd_y.value
    x_cols = list(sel_x.value)
    seg_col = dd_seg.value if dd_seg.value != '-- None --' else None
    
    mapping_locked = True
    
    # Disable controls
    dd_resp.disabled = True
    dd_task.disabled = True
    dd_y.disabled = True
    dd_seg.disabled = True
    sel_x.disabled = True
    btn_lock.disabled = True
    btn_auto.disabled = True
    
    with out_mapping:
        clear_output()
        print("="*60)
        print("COLUMN MAPPING LOCKED")
        print("="*60)
        print(f"  Respondent ID : {resp_col}")
        print(f"  Task/Profile  : {task_col}")
        print(f"  Y variable    : {y_col}")
        print(f"  X attributes  : {x_cols}")
        if seg_col:
            print(f"  Segment       : {seg_col}")
        
        n_resp = df[resp_col].nunique()
        n_tasks = df[task_col].nunique()
        print(f"\n  Respondents   : {n_resp}")
        print(f"  Tasks/profiles: {n_tasks}")
        print(f"  Rows per resp : {len(df) / n_resp:.1f}")
        
        # Check balance
        tasks_per_resp = df.groupby(resp_col)[task_col].nunique()
        print(f"  Tasks per resp: {tasks_per_resp.min()}-{tasks_per_resp.max()} (mean {tasks_per_resp.mean():.1f})")
        if tasks_per_resp.std() > 0.5:
            print("  ⚠️  Warning: unbalanced design (some respondents see fewer tasks)")
        
        print("\n✅ Mapping locked. Run analysis next.")

def on_reset(_):
    global mapping_locked, resp_col, task_col, y_col, x_cols, seg_col
    
    mapping_locked = False
    resp_col = task_col = y_col = seg_col = None
    x_cols = []
    
    dd_resp.disabled = False
    dd_task.disabled = False
    dd_y.disabled = False
    dd_seg.disabled = False
    sel_x.disabled = False
    btn_lock.disabled = False
    btn_auto.disabled = False
    
    status_html.value = "<i>Select mandatory fields (*), then lock.</i>"
    
    with out_mapping:
        clear_output()
        build_mapping_ui()
    
    with out_analysis:
        clear_output()
    with out_viz:
        clear_output()

btn_auto.on_click(on_auto)
btn_lock.on_click(on_lock)
btn_reset.on_click(on_reset)

# =============================================================================
# PHASE 3: RUN ANALYSIS
# =============================================================================

btn_run = widgets.Button(description='▶ Run Analysis', button_style='success', layout=widgets.Layout(width='200px'))

def make_dummies(df_in, cols):
    """Create dummy variables for selected categorical columns."""
    out = df_in.copy()
    dummy_cols = []
    
    for col in cols:
        unique_vals = sorted(df_in[col].dropna().unique())
        if len(unique_vals) < 2:
            print(f"  ⚠️  Skipping '{col}': only 1 level")
            continue
        
        ref = unique_vals[0]
        for val in unique_vals[1:]:
            safe_val = str(val).replace(' ', '_').replace('.', '_')
            dummy_name = f"d_{col}_{safe_val}"
            out[dummy_name] = (df_in[col] == val).astype(int)
            dummy_cols.append(dummy_name)
        
        print(f"  {col}: ref='{ref}', {len(unique_vals)-1} dummies")
    
    return out, dummy_cols

def compute_importance(row, attr_map):
    importance = {}
    for attr, dummies_list in attr_map.items():
        pws = [row.get(d, 0) for d in dummies_list]
        if len(pws) > 0:
            importance[attr] = max(pws) - min(pws)
    total = sum(importance.values())
    if total == 0:
        return {k: 0 for k in importance}
    return {k: v/total*100 for k, v in importance.items()}

def on_run(_):
    global dummies, ib_df, agg_model, attr_map
    
    with out_analysis:
        clear_output()
        
        if not mapping_locked:
            print("❌ Lock column mapping in Step 2 first.")
            return
        
        print("="*60)
        print("RUNNING METRIC CONJOINT ANALYSIS")
        print("="*60)
        
        # Create dummies
        print("\n--- Creating Dummy Variables ---")
        dummies, dummy_cols = make_dummies(df, x_cols)
        
        if len(dummy_cols) == 0:
            print("❌ No valid dummy variables created.")
            return
        
        attr_map = {}
        for col in x_cols:
            attr_map[col] = [d for d in dummy_cols if d.startswith(f"d_{col}_")]
        
        print(f"\nTotal dummies: {len(dummy_cols)}")
        
        # Aggregate OLS
        print("\n--- Aggregate OLS ---")
        X = dummies[dummy_cols].values
        y = dummies[y_col].values
        
        agg_model = LinearRegression()
        agg_model.fit(X, y)
        
        print(f"Intercept: {agg_model.intercept_:.3f}")
        print("\nPart-worths:")
        for col, coef in zip(dummy_cols, agg_model.coef_):
            print(f"  {col:30s}: {coef:7.3f}")
        
        # Importance
        agg_pws = {'Intercept': agg_model.intercept_}
        for d, c in zip(dummy_cols, agg_model.coef_):
            agg_pws[d] = c
        
        imp = {}
        for attr, dlist in attr_map.items():
            pws = [agg_pws.get(d, 0) for d in dlist]
            imp[attr] = max(pws) - min(pws)
        total_imp = sum(imp.values())
        
        print("\nAttribute Importance (%):")
        for attr, val in sorted(imp.items(), key=lambda x: -x[1]):
            print(f"  {attr:20s}: {val/total_imp*100:5.1f}%")
        
        # Individual models
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
        print(f"Estimated: {n_estimated}, Skipped: {n_skipped}")
        
        # Importance per person
        imp_records = []
        for _, row in ib_df.iterrows():
            imp_records.append(compute_importance(row, attr_map))
        
        imp_df = pd.DataFrame(imp_records)
        imp_df[resp_col] = ib_df[resp_col].values
        
        print("\nMean importance:")
        print(imp_df.drop(resp_col, axis=1).mean().round(1).sort_values(ascending=False))
        
        # Store globals
        import builtins
        builtins.ib_df = ib_df
        builtins.imp_df = imp_df
        builtins.attr_map = attr_map
        builtins.dummy_cols = dummy_cols
        builtins.metric_tool_resp_col = resp_col
        builtins.metric_tool_seg_col = seg_col
        
        print("\n✅ Analysis complete.")
    
    with out_viz:
        clear_output()
        render_visualizations()

btn_run.on_click(on_run)

# =============================================================================
# PHASE 4: VISUALIZATIONS
# =============================================================================

def render_visualizations():
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    
    # Plot 1: Boxplot
    ax = axes[0, 0]
    mean_imp = imp_df.drop(resp_col, axis=1).mean().sort_values(ascending=False)
    top_attrs = list(mean_imp.index[:min(4, len(mean_imp))])
    
    box_data, box_labels = [], []
    for attr in top_attrs:
        dlist = attr_map.get(attr, [])
        for d in dlist[:2]:
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
        ax.text(0.5, 0.5, 'No part-worths', ha='center', transform=ax.transAxes)
    
    # Plot 2: Scatter
    ax = axes[0, 1]
    all_d = [d for dlist in attr_map.values() for d in dlist if d in ib_df.columns]
    if len(all_d) >= 2:
        dm = [(d, ib_df[d].abs().mean()) for d in all_d]
        dm.sort(key=lambda x: -x[1])
        d1, d2 = dm[0][0], dm[1][0]
        
        seg_data = None
        if seg_col and seg_col in df.columns:
            seg_map = df.groupby(resp_col)[seg_col].first().to_dict()
            ib_df['_seg'] = ib_df[resp_col].map(seg_map)
            segs = ib_df['_seg'].dropna().unique()
            colors = ['#2c7a7b', '#d69e2e', '#e53e3e', '#805ad5', '#dd6b20']
            for i, seg in enumerate(segs[:5]):
                mask = ib_df['_seg'] == seg
                ax.scatter(ib_df.loc[mask, d1], ib_df.loc[mask, d2],
                          alpha=0.4, s=25, c=colors[i], label=str(seg))
            ax.legend(title=seg_col)
        else:
            ax.scatter(ib_df[d1], ib_df[d2], alpha=0.4, s=25, c='#718096')
        
        ax.set_xlabel(d1.replace('d_', '').replace('_', ' ')[:25])
        ax.set_ylabel(d2.replace('d_', '').replace('_', ' ')[:25])
        ax.set_title('Preference Landscape')
        ax.axhline(0, color='gray', linestyle='--', alpha=0.3)
        ax.axvline(0, color='gray', linestyle='--', alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'Need ≥2 dummies', ha='center', transform=ax.transAxes)
    
    # Plot 3: Segment importance
    ax = axes[1, 0]
    if seg_col and len(top_attrs) > 0:
        imp_df['_seg'] = imp_df[resp_col].map(seg_map)
        si = imp_df.groupby('_seg')[top_attrs].mean()
        x = np.arange(len(top_attrs))
        w = 0.8 / len(si)
        colors = ['#2c7a7b', '#d69e2e', '#e53e3e', '#805ad5', '#dd6b20']
        for i, (seg, color) in enumerate(zip(si.index, colors)):
            ax.bar(x + i*w, si.loc[seg], w, label=str(seg), color=color, edgecolor='black')
        ax.set_xticks(x + w*(len(si)-1)/2)
        ax.set_xticklabels(top_attrs, rotation=15, ha='right')
        ax.set_ylabel('Importance (%)')
        ax.set_title('Importance by Segment')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'No segment labels', ha='center', transform=ax.transAxes)
    
    # Plot 4: Chasm map or correlation
    ax = axes[1, 1]
    price_d = [d for d in dummy_cols if any(k in d.lower() for k in ['price', 'cost'])]
    tech_d = [d for d in dummy_cols if any(k in d.lower() for k in ['smart', 'tech', 'feature', 'advanced'])]
    
    if price_d and tech_d and seg_col:
        ib_df['Price_Sens'] = ib_df[price_d].max(axis=1) - ib_df[price_d].min(axis=1)
        ib_df['Tech_App'] = ib_df[tech_d].mean(axis=1)
        for seg, color in zip(ib_df['_seg'].unique(), colors):
            mask = ib_df['_seg'] == seg
            ax.scatter(ib_df.loc[mask, 'Price_Sens'], ib_df.loc[mask, 'Tech_App'],
                      alpha=0.4, s=30, c=color, label=str(seg))
        ax.set_xlabel('Price Sensitivity')
        ax.set_ylabel('Tech Appetite')
        ax.set_title('Chasm Map')
        ax.legend(title=seg_col)
        ax.axhline(0, color='gray', linestyle='--', alpha=0.3)
        ax.axvline(0, color='gray', linestyle='--', alpha=0.3)
    elif len(top_attrs) >= 2:
        corr = imp_df[top_attrs].corr()
        im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
        ax.set_xticks(range(len(top_attrs)))
        ax.set_yticks(range(len(top_attrs)))
        ax.set_xticklabels(top_attrs, rotation=45, ha='right')
        ax.set_yticklabels(top_attrs)
        ax.set_title('Importance Correlations')
        plt.colorbar(im, ax=ax)
    else:
        ax.text(0.5, 0.5, 'Need price+tech for chasm map', ha='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*60)
    print("DISCUSSION QUESTIONS")
    print("="*60)
    print("""
1. DISPERSION: Which attribute has the widest spread?
   → Wide spread = segmentation opportunity.

2. TRIBES: Are there distinct clouds in the scatter?
   → Clouds = preference tribes.

3. SEGMENTS: Do bars diverge on any attribute?
   → Divergence = chasm location.

4. YOUR PRODUCT: Where is your product on the chasm map?
    """)

# =============================================================================
# ASSEMBLE
# =============================================================================

full_ui = widgets.VBox([
    widgets.HTML("<h2>Generic Metric Conjoint Analysis Tool</h2>"),
    upload_ui,
    widgets.HTML("<hr>"),
    out_mapping,
    widgets.HTML("<hr>"),
    widgets.VBox([widgets.HTML("<h3>Step 3 — Run Analysis</h3>"), btn_run, out_analysis]),
    widgets.HTML("<hr>"),
    out_viz
])

display(full_ui)
