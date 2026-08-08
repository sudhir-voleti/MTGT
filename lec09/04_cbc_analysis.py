# ═══════════════════════════════════════════════════════════════════
#  STEP 4: Generic CBC Analysis Tool — MNL + WTP
# ═══════════════════════════════════════════════════════════════════

import io
import numpy as np
import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from sklearn.linear_model import LogisticRegression

# =============================================================================
# STATE
# =============================================================================

cbc_df = None
pw_df = None       # optional: from Step 2/3 for segment-specific models
seg_col = None

# =============================================================================
# WIDGETS
# =============================================================================

# --- Source panel ---
use_inherited = widgets.Checkbox(value=False, description='Use caselet CBC data', disabled=True)
upload_cbc = widgets.FileUpload(accept='.csv', multiple=False, description='📁 CBC CSV', 
                                button_style='primary', layout=widgets.Layout(width='280px'))
upload_pw = widgets.FileUpload(accept='.csv', multiple=False, description='📁 Part-Worths (opt)', 
                               button_style='info', layout=widgets.Layout(width='280px'))

btn_source = widgets.Button(description='▶ Confirm Source', button_style='success')
source_status = widgets.HTML("Upload CBC CSV or check auto-detect.")

source_panel = widgets.VBox([
    widgets.HTML("<h2>CBC Analysis Tool: Step 1 — Data Source</h2>"),
    widgets.HTML("<p>Upload CBC data (one row per alternative per task). Optional: part-worths for segment-specific models.</p>"),
    widgets.HBox([use_inherited, upload_cbc, upload_pw, btn_source]),
    source_status
])

# --- Mapping panel ---
dd_resp = widgets.Dropdown(options=[], description='Resp ID*:', layout=widgets.Layout(width='260px'))
dd_task = widgets.Dropdown(options=[], description='Task ID*:', layout=widgets.Layout(width='260px'))
dd_alt = widgets.Dropdown(options=[], description='Alt ID*:', layout=widgets.Layout(width='260px'))
dd_choice = widgets.Dropdown(options=[], description='Chosen*:', layout=widgets.Layout(width='260px'))
dd_seg = widgets.Dropdown(options=['-- None --'], description='Segment:', layout=widgets.Layout(width='260px'))

sel_attr = widgets.SelectMultiple(options=[], description='Attributes*:', rows=6, 
                                  layout=widgets.Layout(width='320px', height='200px'))

btn_lock = widgets.Button(description='🔒 Lock & Estimate MNL', button_style='success', disabled=True)
btn_reset = widgets.Button(description='🗑 Reset', button_style='warning')

mapping_status = widgets.HTML("<i>Confirm data source first.</i>")

mapping_controls = widgets.VBox([
    widgets.HTML("<h3>Step 2 — Map Columns</h3>"),
    widgets.HTML("<p>Required: Resp ID, Task ID, Alt ID, Chosen (0/1), attribute columns.<br>Optional: segment for heterogeneity.</p>"),
    widgets.HBox([dd_resp, dd_task, dd_alt, dd_choice, dd_seg]),
    sel_attr,
    widgets.HBox([btn_lock, btn_reset]),
    mapping_status
])

mapping_panel = widgets.VBox([])

# --- Results ---
results_html = widgets.HTML("")
results_panel = widgets.VBox([results_html])
viz_panel = widgets.VBox([])

# =============================================================================
# AUTO-DETECT: Try to grab cbc_df from caselet namespace
# =============================================================================

try:
    cbc_df = globals()['cbc_df']
    if cbc_df is not None and len(cbc_df) > 0:
        use_inherited.value = True
        use_inherited.disabled = False
        source_status.value = "✅ Auto-detected CBC data. Check box and confirm."
except (KeyError, NameError):
    use_inherited.disabled = True
    source_status.value = "ℹ️ Upload CBC CSV file."

# =============================================================================
# EVENT HANDLERS
# =============================================================================

def on_source(_):
    global cbc_df, pw_df
    
    if use_inherited.value:
        try:
            cbc_df = globals()['cbc_df']
            source_status.value = f"✅ Using caselet CBC: {cbc_df.shape}"
        except (KeyError, NameError):
            source_status.value = "<span style='color:#c53030'>❌ Caselet data not found. Upload CSV.</span>"
            return
    else:
        if not upload_cbc.value:
            source_status.value = "<span style='color:#c53030'>❌ Upload CBC CSV or check auto-detect</span>"
            return
        raw = list(upload_cbc.value.values())[0]['content']
        cbc_df = pd.read_csv(io.BytesIO(raw))
        source_status.value = f"✅ Uploaded CBC: {cbc_df.shape}"
    
    # Optional part-worths
    if upload_pw.value:
        raw2 = list(upload_pw.value.values())[0]['content']
        pw_df = pd.read_csv(io.BytesIO(raw2))
        source_status.value += f" | Part-worths: {pw_df.shape}"
    else:
        pw_df = None
    
    # Populate mapping
    all_cols = list(cbc_df.columns)
    
    dd_resp.options = all_cols
    dd_task.options = all_cols
    dd_alt.options = all_cols
    dd_choice.options = all_cols
    dd_seg.options = ['-- None --'] + all_cols
    
    # Auto-guess
    resp_guess = next((c for c in all_cols if any(k in c.lower() for k in ['resp', 'id', 'subject', 'panelist'])), all_cols[0])
    task_guess = next((c for c in all_cols if any(k in c.lower() for k in ['task', 'profile', 'trial', 'concept'])), all_cols[1] if len(all_cols) > 1 else all_cols[0])
    alt_guess = next((c for c in all_cols if any(k in c.lower() for k in ['alt', 'alternative', 'option'])), all_cols[2] if len(all_cols) > 2 else all_cols[0])
    choice_guess = next((c for c in all_cols if any(k in c.lower() for k in ['chosen', 'choice', 'select', 'pick', 'y'])), all_cols[3] if len(all_cols) > 3 else all_cols[0])
    seg_guess = next((c for c in all_cols if any(k in c.lower() for k in ['segment', 'cluster', 'group'])), '-- None --')
    
    dd_resp.value = resp_guess
    dd_task.value = task_guess
    dd_alt.value = alt_guess
    dd_choice.value = choice_guess
    dd_seg.value = seg_guess if seg_guess in dd_seg.options else '-- None --'
    
    # Auto-guess attributes: non-ID, non-choice columns
    exclude = {resp_guess, task_guess, alt_guess, choice_guess}
    if seg_guess != '-- None --':
        exclude.add(seg_guess)
    
    # Prefer categorical columns for attributes
    cat_cols = [c for c in all_cols if not pd.api.types.is_numeric_dtype(cbc_df[c]) or cbc_df[c].nunique() <= 6]
    attr_candidates = [c for c in cat_cols if c not in exclude]
    
    sel_attr.options = all_cols
    sel_attr.value = tuple(attr_candidates[:min(8, len(attr_candidates))])
    
    source_status.value += f" | {len(attr_candidates)} candidate attributes detected."
    
    btn_lock.disabled = False
    mapping_panel.children = [mapping_controls]

def make_dummies(df_in, cols):
    """Create dummy variables for selected categorical columns."""
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

def on_lock(_):
    global seg_col
    
    if len(sel_attr.value) == 0:
        mapping_status.value = "<span style='color:#c53030'>❌ Select at least one attribute.</span>"
        return
    
    resp_col = dd_resp.value
    task_col = dd_task.value
    alt_col = dd_alt.value
    choice_col = dd_choice.value
    seg_col = dd_seg.value if dd_seg.value != '-- None --' else None
    attr_cols = list(sel_attr.value)
    
    # Validate choice is binary
    if not set(cbc_df[choice_col].dropna().unique()).issubset({0, 1}):
        mapping_status.value = "<span style='color:#c53030'>❌ Choice column must be 0/1.</span>"
        return
    
    # Disable
    dd_resp.disabled = True
    dd_task.disabled = True
    dd_alt.disabled = True
    dd_choice.disabled = True
    dd_seg.disabled = True
    sel_attr.disabled = True
    btn_lock.disabled = True
    
    # Create dummies
    cbc_dummies, dummy_cols = make_dummies(cbc_df, attr_cols)
    
    # Add None dummy (alternative with all attributes = reference)
    cbc_dummies['d_None'] = (cbc_dummies[alt_col] == cbc_dummies[alt_col].max()).astype(int)
    # Actually: None is typically the last alt or a special code. Let user handle via data.
    # Better: detect if there's a "None" level in any attribute
    none_detected = False
    for col in attr_cols:
        if 'None' in cbc_dummies[col].values or 'none' in cbc_dummies[col].values:
            none_detected = True
    
    # Build MNL dataset
    X = cbc_dummies[dummy_cols].values
    y = cbc_dummies[choice_col].values
    
    # Sample weights: 1 / n_alts per task for conditional logit approx
    task_alt_counts = cbc_dummies.groupby([resp_col, task_col]).size().reset_index(name='n_alts')
    cbc_dummies = cbc_dummies.merge(task_alt_counts, on=[resp_col, task_col])
    sample_weights = 1.0 / cbc_dummies['n_alts']
    
    # Aggregate MNL
    mnl_agg = LogisticRegression(max_iter=1000, solver='lbfgs')
    mnl_agg.fit(X, y, sample_weight=sample_weights)
    
    # Results
    lines = []
    lines.append("="*60)
    lines.append("AGGREGATE MULTINOMIAL LOGIT (MNL)")
    lines.append("="*60)
    lines.append(f"Respondents: {cbc_dummies[resp_col].nunique()}")
    lines.append(f"Tasks: {cbc_dummies[task_col].nunique()}")
    lines.append(f"Alternatives: {cbc_dummies[alt_col].nunique()}")
    lines.append(f"Attributes: {len(attr_cols)} → {len(dummy_cols)} dummies")
    
    lines.append("\nCoefficients (log-odds):")
    for col, coef in zip(dummy_cols, mnl_agg.coef_[0]):
        lines.append(f"  {col:30s}: {coef:7.3f}")
    
    # WTP computation
    price_dummies = [d for d in dummy_cols if 'price' in d.lower() or 'cost' in d.lower()]
    if len(price_dummies) > 0:
        beta_price = abs(mnl_agg.coef_[0][dummy_cols.index(price_dummies[0])])
        if beta_price > 0.001:
            lines.append("\nWillingness to Pay (WTP):")
            for d, coef in zip(dummy_cols, mnl_agg.coef_[0]):
                if d not in price_dummies:
                    wtp = -coef / beta_price
                    lines.append(f"  {d:30s}: {wtp:7.3f} (units of price)")
    
    # Segment-specific models
    if seg_col:
        lines.append("\n" + "="*60)
        lines.append("SEGMENT-SPECIFIC MNL")
        lines.append("="*60)
        
        for seg in sorted(cbc_dummies[seg_col].unique()):
            seg_data = cbc_dummies[cbc_dummies[seg_col] == seg]
            X_seg = seg_data[dummy_cols].values
            y_seg = seg_data[choice_col].values
            w_seg = 1.0 / seg_data['n_alts']
            
            mnl_seg = LogisticRegression(max_iter=1000, solver='lbfgs')
            mnl_seg.fit(X_seg, y_seg, sample_weight=w_seg)
            
            lines.append(f"\n{seg} (n={len(seg_data)} rows):")
            for d, c in zip(dummy_cols[:min(6, len(dummy_cols))], mnl_seg.coef_[0][:6]):
                lines.append(f"  {d:25s}: {c:7.3f}")
    
    lines.append("\n✅ MNL estimation complete.")
    
    # Add choice summary
    choice_summary = render_choice_summary(cbc_dummies, attr_cols, choice_col, task_col, resp_col)
    lines.append(choice_summary)
    results_html.value = "<pre style='font-family:monospace; font-size:13px; line-height:1.5;'>" + "\n".join(lines) + "</pre>"
    
    # Store globals
    import builtins
    builtins.cbc_dummies = cbc_dummies
    builtins.mnl_agg = mnl_agg
    builtins.dummy_cols = dummy_cols
    builtins.attr_cols = attr_cols


def render_viz(cbc_dummies, dummy_cols, attr_cols, mnl_agg, choice_col, task_col, resp_col):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Coefficient plot
    ax = axes[0]
    coefs = mnl_agg.coef_[0]
    colors = ['#2c7a7b' if c > 0 else '#e53e3e' for c in coefs]
    y_pos = np.arange(len(dummy_cols))
    ax.barh(y_pos, coefs, color=colors, edgecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels([d.replace('d_', '').replace('_', ' ')[:20] for d in dummy_cols], fontsize=9)
    ax.set_xlabel('Log-Odds Coefficient')
    ax.set_title('MNL Coefficients: What Drives Choice?')
    ax.axvline(0, color='gray', linestyle='--', alpha=0.5)
    
    # Plot 2: Attribute importance from MNL
    ax = axes[1]
    attr_imp = {}
    for attr in attr_cols:
        attr_dummies = [d for d in dummy_cols if d.startswith(f"d_{attr}_")]
        if attr_dummies:
            attr_coefs = [coefs[dummy_cols.index(d)] for d in attr_dummies]
            attr_imp[attr] = max(attr_coefs) - min(attr_coefs)
    
    if attr_imp:
        sorted_imp = sorted(attr_imp.items(), key=lambda x: -x[1])
        names = [x[0] for x in sorted_imp]
        vals = [x[1] for x in sorted_imp]
        colors2 = ['#2c7a7b', '#718096', '#d69e2e', '#e53e3e', '#805ad5', '#dd6b20']
        ax.barh(names[::-1], vals[::-1], color=colors2[:len(names)][::-1], edgecolor='black')
        ax.set_xlabel('Importance (max - min coefficient)')
        ax.set_title('Attribute Importance from MNL')
    else:
        ax.text(0.5, 0.5, 'No attributes to plot', ha='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.show()
    
    # Plot 3: Win rate by attribute levels
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    win_data = []
    win_labels = []
    for attr in attr_cols[:min(4, len(attr_cols))]:
        if attr in cbc_dummies.columns:
            levels = sorted(cbc_dummies[attr].dropna().unique())
            for lvl in levels:
                mask = cbc_dummies[attr] == lvl
                rate = cbc_dummies.loc[mask, choice_col].mean()
                win_data.append(rate)
                win_labels.append(f"{attr[:8]}={str(lvl)[:10]}")
    
    if win_data:
        colors3 = ['#2c7a7b' if r > 0.5 else '#e53e3e' for r in win_data]
        y_pos = np.arange(len(win_data))
        ax2.barh(y_pos, win_data, color=colors3, edgecolor='black')
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(win_labels, fontsize=9)
        ax2.set_xlabel('Choice Rate (fraction of times chosen when shown)')
        ax2.set_title('Win Rate by Attribute Level: What Wins When Shown?')
        ax2.axvline(0.5, color='gray', linestyle='--', alpha=0.5)
        ax2.set_xlim(0, 1)
        plt.tight_layout()
        plt.show()
    
    questions = """
    <div style="background:#fffbeb; border:2px dashed #f59e0b; border-radius:12px; padding:16px; margin:12px 0;">
    <h4 style="margin-top:0; color:#b45309;">Discussion Questions</h4>
    <ol style="color:#78350f;">
    <li><b>Signs:</b> Which coefficients are positive? Negative? What does that mean for your product?</li>
    <li><b>Price:</b> Is the price coefficient the largest in magnitude? If not, what is?</li>
    <li><b>WTP:</b> Which feature has the highest willingness-to-pay? Is it worth building?</li>
    <li><b>Win Rates:</b> Which attribute level wins most often when shown? Is it the same as the highest coefficient?</li>
    </ol>
    </div>
    """
    viz_panel.children = [widgets.HTML(questions)]

def on_reset(_):
    global seg_col
    
    seg_col = None
    
    dd_resp.disabled = False
    dd_task.disabled = False
    dd_alt.disabled = False
    dd_choice.disabled = False
    dd_seg.disabled = False
    sel_attr.disabled = False
    btn_lock.disabled = False
    
    mapping_status.value = "<i>Confirm data source first.</i>"
    results_html.value = ""
    viz_panel.children = []

def render_viz(cbc_dummies, dummy_cols, attr_cols, mnl_agg):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Coefficient plot
    ax = axes[0]
    coefs = mnl_agg.coef_[0]
    colors = ['#2c7a7b' if c > 0 else '#e53e3e' for c in coefs]
    y_pos = np.arange(len(dummy_cols))
    ax.barh(y_pos, coefs, color=colors, edgecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels([d.replace('d_', '').replace('_', ' ')[:20] for d in dummy_cols], fontsize=9)
    ax.set_xlabel('Log-Odds Coefficient')
    ax.set_title('MNL Coefficients: What Drives Choice?')
    ax.axvline(0, color='gray', linestyle='--', alpha=0.5)
    
    # Plot 2: Attribute importance from MNL
    ax = axes[1]
    attr_imp = {}
    for attr in attr_cols:
        attr_dummies = [d for d in dummy_cols if d.startswith(f"d_{attr}_")]
        if attr_dummies:
            attr_coefs = [coefs[dummy_cols.index(d)] for d in attr_dummies]
            attr_imp[attr] = max(attr_coefs) - min(attr_coefs)
    
    if attr_imp:
        sorted_imp = sorted(attr_imp.items(), key=lambda x: -x[1])
        names = [x[0] for x in sorted_imp]
        vals = [x[1] for x in sorted_imp]
        colors2 = ['#2c7a7b', '#718096', '#d69e2e', '#e53e3e', '#805ad5', '#dd6b20']
        ax.barh(names[::-1], vals[::-1], color=colors2[:len(names)][::-1], edgecolor='black')
        ax.set_xlabel('Importance (max - min coefficient)')
        ax.set_title('Attribute Importance from MNL')
    else:
        ax.text(0.5, 0.5, 'No attributes to plot', ha='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.show()


    # Plot 3: Win rate by top attribute levels
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    win_data = []
    win_labels = []
    for attr in attr_cols[:min(4, len(attr_cols))]:
        if attr in cbc_dummies.columns:
            levels = sorted(cbc_dummies[attr].dropna().unique())
            for lvl in levels:
                mask = cbc_dummies[attr] == lvl
                rate = cbc_dummies.loc[mask, choice_col].mean()
                win_data.append(rate)
                win_labels.append(f"{attr[:8]}={str(lvl)[:10]}")
    
    if win_data:
        colors3 = ['#2c7a7b' if r > 0.5 else '#e53e3e' for r in win_data]
        y_pos = np.arange(len(win_data))
        ax2.barh(y_pos, win_data, color=colors3, edgecolor='black')
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(win_labels, fontsize=9)
        ax2.set_xlabel('Choice Rate (fraction of times chosen when shown)')
        ax2.set_title('Win Rate by Attribute Level: What Wins When Shown?')
        ax2.axvline(0.5, color='gray', linestyle='--', alpha=0.5)
        ax2.set_xlim(0, 1)
        plt.tight_layout()
        plt.show()
    
    questions = """
    <div style="background:#fffbeb; border:2px dashed #f59e0b; border-radius:12px; padding:16px; margin:12px 0;">
    <h4 style="margin-top:0; color:#b45309;">Discussion Questions</h4>
    <ol style="color:#78350f;">
    <li><b>Signs:</b> Which coefficients are positive? Negative? What does that mean for your product?</li>
    <li><b>Price:</b> Is the price coefficient the largest in magnitude? If not, what is?</li>
    <li><b>WTP:</b> Which feature has the highest willingness-to-pay? Is it worth building?</li>
    <li><b>Segments:</b> Do segment-specific models differ from aggregate? Where is heterogeneity?</li>
    </ol>
    </div>
    """
    viz_panel.children = [widgets.HTML(questions)]

# =============================================================================
# WIRE & ASSEMBLE
# =============================================================================

btn_source.on_click(on_source)
btn_lock.on_click(on_lock)
btn_reset.on_click(on_reset)

full_ui = widgets.VBox([
    source_panel,
    mapping_panel,
    results_panel,
    viz_panel
])

display(full_ui)
