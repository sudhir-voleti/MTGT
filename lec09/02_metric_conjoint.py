# ═══════════════════════════════════════════════════════════════════
#  STEP 2: Generic Metric Conjoint Analysis Tool (MVP) — FIXED v2
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
seg_col = None

dummies = None
ib_df = None
agg_model = None
attr_map = {}

# =============================================================================
# WIDGETS (all declared upfront, no Output widgets for dynamic content)
# =============================================================================

# --- Upload panel ---
upload_widget = widgets.FileUpload(
    accept='.csv', multiple=False, description='📁 Upload CSV',
    button_style='primary', layout=widgets.Layout(width='300px'))

btn_load = widgets.Button(description='▶ Load CSV', button_style='success')
upload_status = widgets.HTML("Upload your conjoint CSV to begin.")

upload_panel = widgets.VBox([
    widgets.HTML("<h2>Metric Conjoint Tool: Step 1 — Upload</h2>"),
    widgets.HTML("<p>Required: respondent ID, task/profile ID, Y variable, attribute columns.<br>Optional: segment label.</p>"),
    widgets.HBox([upload_widget, btn_load]),
    upload_status
])

# --- Mapping panel (initially empty, populated after upload) ---
dd_resp = widgets.Dropdown(options=[], description='Resp ID*:', layout=widgets.Layout(width='260px'))
dd_task = widgets.Dropdown(options=[], description='Task ID*:', layout=widgets.Layout(width='260px'))
dd_y = widgets.Dropdown(options=[], description='Y (rating)*:', layout=widgets.Layout(width='260px'))
dd_seg = widgets.Dropdown(options=['-- None --'], description='Segment:', layout=widgets.Layout(width='260px'))
sel_x = widgets.SelectMultiple(options=[], description='Attributes*:', rows=6, layout=widgets.Layout(width='300px', height='200px'))

btn_auto = widgets.Button(description='💡 Auto-Detect', button_style='info')
btn_lock = widgets.Button(description='🔒 Lock Mapping', button_style='success', disabled=True)
btn_reset = widgets.Button(description='🗑 Reset', button_style='warning')

mapping_status = widgets.HTML("<i>Select mandatory fields (*), then lock.</i>")

mapping_controls = widgets.VBox([
    widgets.HTML("<h3>Step 2 — Map Columns</h3>"),
    widgets.HTML("<p><b>Required (*):</b> Respondent ID, Task/Profile ID, Y variable, ≥1 X attribute.<br><b>Optional:</b> Segment label for validation.</p>"),
    widgets.HBox([dd_resp, dd_task, dd_y, dd_seg]),
    sel_x,
    widgets.HBox([btn_auto, btn_lock, btn_reset]),
    mapping_status
])

# Start with mapping panel hidden
mapping_panel = widgets.VBox([])

# --- Analysis panel ---
btn_run = widgets.Button(description='▶ Run Analysis', button_style='success', layout=widgets.Layout(width='200px'), disabled=True)
analysis_status = widgets.HTML("<i>Lock mapping first, then run analysis.</i>")

analysis_panel = widgets.VBox([
    widgets.HTML("<h3>Step 3 — Run Analysis</h3>"),
    widgets.HBox([btn_run, analysis_status])
])

# --- Results panel (for text output) ---
results_text = widgets.HTML("")
results_panel = widgets.VBox([results_text])

# --- Viz panel (matplotlib renders here) ---
viz_panel = widgets.VBox([])

# =============================================================================
# EVENT HANDLERS
# =============================================================================

def on_load(_):
    global df
    
    if not upload_widget.value:
        upload_status.value = "<span style='color:#c53030'>❌ Select a CSV file first.</span>"
        return
    
    raw = list(upload_widget.value.values())[0]['content']
    df = pd.read_csv(io.BytesIO(raw))
    
    upload_status.value = f"✅ Loaded: {df.shape[0]} rows × {df.shape[1]} columns. Columns: {', '.join(df.columns)}"
    
    # Populate mapping panel
    all_cols = list(df.columns)
    numeric_cols = [c for c in all_cols if pd.api.types.is_numeric_dtype(df[c])]
    
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
    
    exclude = {resp_guess, task_guess, y_guess}
    if seg_guess != '-- None --':
        exclude.add(seg_guess)
    auto_x = [c for c in all_cols if c not in exclude]
    sel_x.value = tuple(auto_x)
    
    btn_lock.disabled = False
    
    # Show mapping panel
    mapping_panel.children = [mapping_controls]

def check_mandatory():
    if dd_resp.value is None or dd_resp.value == '':
        return "Select Respondent ID"
    if dd_task.value is None or dd_task.value == '':
        return "Select Task/Profile ID"
    if dd_y.value is None or dd_y.value == '':
        return "Select Y variable"
    if len(sel_x.value) == 0:
        return "Select at least one X attribute"
    if dd_resp.value == dd_task.value:
        return "Resp ID and Task ID must be different"
    if dd_y.value in sel_x.value:
        return "Y cannot also be an X attribute"
    return None

def on_lock(_):
    global mapping_locked, resp_col, task_col, y_col, x_cols, seg_col
    
    err = check_mandatory()
    if err:
        mapping_status.value = f"<span style='color:#c53030'>❌ {err}</span>"
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
    
    # Summary
    n_resp = df[resp_col].nunique()
    n_tasks = df[task_col].nunique()
    tasks_per_resp = df.groupby(resp_col)[task_col].nunique()
    
    summary = f"""
    <div style="background:#f0fdf4; border-left:4px solid #16a34a; padding:12px 16px; margin:8px 0;">
    <b>✅ Mapping Locked</b><br>
    Respondent ID: <code>{resp_col}</code> | Task ID: <code>{task_col}</code> | Y: <code>{y_col}</code><br>
    X attributes: {', '.join(x_cols)}<br>
    Segment: {seg_col if seg_col else '(none)'}<br>
    Respondents: {n_resp} | Tasks: {n_tasks} | Rows/resp: {len(df)/n_resp:.1f}
    </div>
    """
    mapping_status.value = summary
    
    # Enable run
    btn_run.disabled = False
    analysis_status.value = "<i>Ready to run analysis.</i>"

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
    
    mapping_status.value = "<i>Select mandatory fields (*), then lock.</i>"
    btn_run.disabled = True
    analysis_status.value = "<i>Lock mapping first.</i>"
    results_text.value = ""
    viz_panel.children = []

def on_auto(_):
    on_load(None)  # Re-run auto-detect

def make_dummies(df_in, cols):
    out = df_in.copy()
    dummy_cols = []
    for col in cols:
        unique_vals = sorted(df_in[col].dropna().unique())
        if len(unique_vals) < 2:
            continue
        ref = unique_vals[0]
        for val in unique_vals[1:]:
            safe_val = str(val).replace(' ', '_').replace('.', '_')
            dummy_name = f"d_{col}_{safe_val}"
            out[dummy_name] = (df_in[col] == val).astype(int)
            dummy_cols.append(dummy_name)
    return out, dummy_cols

def compute_importance(row, attr_map):
    importance = {}
    for attr, dlist in attr_map.items():
        pws = [row.get(d, 0) for d in dlist]
        if len(pws) > 0:
            importance[attr] = max(pws) - min(pws)
    total = sum(importance.values())
    if total == 0:
        return {k: 0 for k in importance}
    return {k: v/total*100 for k, v in importance.items()}

def on_run(_):
    global dummies, ib_df, agg_model, attr_map
    
    if not mapping_locked:
        results_text.value = "<span style='color:#c53030'>❌ Lock mapping first.</span>"
        return
    
    # Build results as HTML string
    lines = []
    lines.append("=" * 60)
    lines.append("RUNNING METRIC CONJOINT ANALYSIS")
    lines.append("=" * 60)
    
    dummies, dummy_cols = make_dummies(df, x_cols)
    attr_map = {col: [d for d in dummy_cols if d.startswith(f"d_{col}_")] for col in x_cols}
    
    lines.append(f"\nDummy variables created: {len(dummy_cols)}")
    
    # Aggregate OLS
    X = dummies[dummy_cols].values
    y = dummies[y_col].values
    agg_model = LinearRegression()
    agg_model.fit(X, y)
    
    lines.append(f"\nIntercept: {agg_model.intercept_:.3f}")
    lines.append("\nPart-worths:")
    for col, coef in zip(dummy_cols, agg_model.coef_):
        lines.append(f"  {col:30s}: {coef:7.3f}")
    
    # Importance
    agg_pws = {'Intercept': agg_model.intercept_}
    for d, c in zip(dummy_cols, agg_model.coef_):
        agg_pws[d] = c
    imp = {}
    for attr, dlist in attr_map.items():
        pws = [agg_pws.get(d, 0) for d in dlist]
        imp[attr] = max(pws) - min(pws)
    total_imp = sum(imp.values())
    
    lines.append("\nAttribute Importance (%):")
    for attr, val in sorted(imp.items(), key=lambda x: -x[1]):
        lines.append(f"  {attr:20s}: {val/total_imp*100:5.1f}%")
    
    # Individual models
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
    lines.append(f"\nIndividual models: {n_estimated} estimated, {n_skipped} skipped")
    
    # Per-person importance
    imp_records = []
    for _, row in ib_df.iterrows():
        imp_records.append(compute_importance(row, attr_map))
    imp_df = pd.DataFrame(imp_records)
    imp_df[resp_col] = ib_df[resp_col].values
    
    lines.append("\nMean importance:")
    for attr, val in imp_df.drop(resp_col, axis=1).mean().round(1).sort_values(ascending=False).items():
        lines.append(f"  {attr:20s}: {val:5.1f}%")
    
    # Store globals
    import builtins
    builtins.ib_df = ib_df
    builtins.imp_df = imp_df
    builtins.attr_map = attr_map
    builtins.dummy_cols = dummy_cols
    builtins.metric_tool_resp_col = resp_col
    builtins.metric_tool_seg_col = seg_col
    
    lines.append("\n✅ Analysis complete.")
    results_text.value = "<pre style='font-family:monospace; font-size:13px; line-height:1.5;'>" + "\n".join(lines) + "</pre>"
    
    # Render viz
    render_viz()

def render_viz():
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
    
    # Discussion questions as HTML
    questions = """
    <div style="background:#fffbeb; border:2px dashed #f59e0b; border-radius:12px; padding:16px; margin:12px 0;">
    <h4 style="margin-top:0; color:#b45309;">Discussion Questions</h4>
    <ol style="color:#78350f;">
    <li><b>Dispersion:</b> Which attribute has the widest spread? → Wide spread = segmentation opportunity.</li>
    <li><b>Tribes:</b> Are there distinct clouds in the scatter? → Clouds = preference tribes.</li>
    <li><b>Segments:</b> Do bars diverge on any attribute? → Divergence = chasm location.</li>
    <li><b>Your Product:</b> Where is your product on the chasm map?</li>
    </ol>
    </div>
    """
    viz_panel.children = [widgets.HTML(questions)]

# =============================================================================
# WIRE EVENTS
# =============================================================================

btn_load.on_click(on_load)
btn_auto.on_click(on_auto)
btn_lock.on_click(on_lock)
btn_reset.on_click(on_reset)
btn_run.on_click(on_run)

# =============================================================================
# ASSEMBLE UI
# =============================================================================

full_ui = widgets.VBox([
    upload_panel,
    mapping_panel,
    analysis_panel,
    results_panel,
    viz_panel
])

display(full_ui)
