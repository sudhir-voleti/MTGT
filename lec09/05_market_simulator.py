# ═══════════════════════════════════════════════════════════════════
#  STEP 5: Generic Market Simulator — Share Prediction + Traction + CLV
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

mnl_model = None      # from Step 4 or uploaded
dummy_cols = None     # from Step 4 or uploaded
attr_cols = None      # from Step 4 or uploaded
seg_col = None

# =============================================================================
# WIDGETS
# =============================================================================

# --- Source panel ---
use_inherited = widgets.Checkbox(value=False, description='Use Step 4 MNL', disabled=True)
upload_mnl = widgets.FileUpload(accept='.csv', multiple=False, description='📁 MNL Coefficients', 
                                button_style='primary', layout=widgets.Layout(width='280px'))
upload_scenarios = widgets.FileUpload(accept='.csv', multiple=False, description='📁 Scenarios (opt)', 
                                      button_style='info', layout=widgets.Layout(width='280px'))

btn_source = widgets.Button(description='▶ Confirm Source', button_style='success')
source_status = widgets.HTML("Upload MNL coefficients or check auto-detect.")

source_panel = widgets.VBox([
    widgets.HTML("<h2>Market Simulator: Step 1 — Load MNL Model</h2>"),
    widgets.HTML("<p>Upload coefficient CSV (from Step 4) or auto-detect. Optional: upload scenario definitions.</p>"),
    widgets.HBox([use_inherited, upload_mnl, upload_scenarios, btn_source]),
    source_status
])

# --- Scenario builder panel ---
scenario_rows = []

# Build dynamic attribute selectors from detected columns
attr_selectors = {}  # populated after source load
scenario_list = widgets.VBox([])

btn_add_scenario = widgets.Button(description='➕ Add Scenario', button_style='info', disabled=True)
btn_simulate = widgets.Button(description='▶ Simulate Market', button_style='success', disabled=True)
btn_reset = widgets.Button(description='🗑 Reset', button_style='warning')

scenario_status = widgets.HTML("<i>Load MNL model first.</i>")

scenario_panel = widgets.VBox([
    widgets.HTML("<h3>Step 2 — Build Scenarios</h3>"),
    widgets.HTML("<p>Define product configurations to simulate. Add competitors and your own SKUs.</p>"),
    scenario_list,
    widgets.HBox([btn_add_scenario, btn_simulate, btn_reset]),
    scenario_status
])

scenario_container = widgets.VBox([])

# --- Results ---
results_html = widgets.HTML("")
results_panel = widgets.VBox([results_html])
viz_panel = widgets.VBox([])

# =============================================================================
# AUTO-DETECT
# =============================================================================

inherited_ok = False
try:
    mnl_model = globals().get('mnl_agg', None)
    dummy_cols = globals().get('dummy_cols', None)
    attr_cols = globals().get('attr_cols', None)
    if mnl_model is not None and dummy_cols is not None and attr_cols is not None:
        inherited_ok = True
        use_inherited.value = True
        use_inherited.disabled = False
        source_status.value = "✅ Auto-detected MNL from Step 4. Check box and confirm."
except Exception as e:
    pass

if not inherited_ok:
    use_inherited.disabled = True
    use_inherited.value = False
    source_status.value = "ℹ️ Upload MNL coefficient CSV from Step 4."

# =============================================================================
# EVENT HANDLERS
# =============================================================================

def on_source(_):
    global mnl_model, dummy_cols, attr_cols, seg_col
    
    if use_inherited.value:
        try:
            mnl_model = globals()['mnl_agg']
            dummy_cols = globals()['dummy_cols']
            attr_cols = globals()['attr_cols']
            source_status.value = f"✅ Using Step 4 MNL: {len(dummy_cols)} dummies, {len(attr_cols)} attributes"
        except (KeyError, NameError):
            source_status.value = "<span style='color:#c53030'>❌ Step 4 results not found. Upload CSV.</span>"
            return
    else:
        if not upload_mnl.value:
            source_status.value = "<span style='color:#c53030'>❌ Upload MNL CSV or check auto-detect</span>"
            return
        raw = list(upload_mnl.value.values())[0]['content']
        coef_df = pd.read_csv(io.BytesIO(raw))
        # Expect columns: dummy_name, coefficient
        dummy_cols = coef_df['dummy_name'].tolist()
        coefs = coef_df['coefficient'].values
        # Reconstruct simple model
        class SimpleModel:
            def __init__(self, c):
                self.coef_ = np.array([c])
                self.intercept_ = 0
        mnl_model = SimpleModel(coefs)
        attr_cols = list(set([d.split('_')[1] for d in dummy_cols if d.startswith('d_')]))
        source_status.value = f"✅ Uploaded MNL: {len(dummy_cols)} dummies"
    
    # Build scenario UI
    build_scenario_ui()
    
    btn_add_scenario.disabled = False
    btn_simulate.disabled = False
    scenario_container.children = [scenario_panel]

def build_scenario_ui():
    global attr_selectors
    
    # Parse dummy names to get attribute levels
    attr_levels = {}
    for d in dummy_cols:
        if not d.startswith('d_'):
            continue
        parts = d[2:].split('_')
        if len(parts) >= 2:
            attr = parts[0]
            level = '_'.join(parts[1:])
            if attr not in attr_levels:
                attr_levels[attr] = ['(reference)']
            attr_levels[attr].append(level)
    
    # Create dropdowns for each attribute
    attr_selectors = {}
    for attr in attr_cols:
        levels = attr_levels.get(attr, ['(reference)', 'level1', 'level2'])
        dd = widgets.Dropdown(options=levels, value=levels[0], description=f'{attr}:', 
                              layout=widgets.Layout(width='220px'))
        attr_selectors[attr] = dd

def add_scenario_row(_):
    if not attr_selectors:
        return
    
    txt_name = widgets.Text(value=f"Scenario {len(scenario_rows)+1}", description='Name:', 
                            layout=widgets.Layout(width='200px'))
    selectors = widgets.HBox([attr_selectors[a] for a in attr_cols[:min(4, len(attr_cols))]])
    
    row = widgets.VBox([widgets.HBox([txt_name, selectors])])
    scenario_rows.append({'name': txt_name, 'selectors': {a: attr_selectors[a] for a in attr_cols}})
    scenario_list.children = [r['name'].parent for r in scenario_rows]  # Simplified

# Simpler: just use the current selector values
def on_simulate(_):
    global seg_col
    
    if mnl_model is None:
        scenario_status.value = "<span style='color:#c53030'>❌ Load MNL model first.</span>"
        return
    
    # Build scenario from current selector values
    scenario = {}
    for attr, selector in attr_selectors.items():
        scenario[attr] = selector.value
    
    # Compute utility
    def scenario_to_dummies(scenario):
        d = np.zeros(len(dummy_cols))
        for i, dummy in enumerate(dummy_cols):
            if not dummy.startswith('d_'):
                continue
            parts = dummy[2:].split('_')
            attr = parts[0]
            level = '_'.join(parts[1:])
            if attr in scenario and scenario[attr] == level:
                d[i] = 1
        return d
    
    # Simulate against competitors
    lines = []
    lines.append("="*60)
    lines.append("MARKET SIMULATION")
    lines.append("="*60)
    
    # Your product
    your_dummies = scenario_to_dummies(scenario)
    your_u = mnl_model.coef_[0].dot(your_dummies) + getattr(mnl_model, 'intercept_', 0)
    
    lines.append(f"\nYour Product: {scenario}")
    lines.append(f"Utility: {your_u:.3f}")
    
    # Competitor defaults (can be overridden)
    competitors = {
        'Competitor A': {a: '(reference)' for a in attr_cols},
        'Competitor B': {a: '(reference)' for a in attr_cols},
        'None': {a: '(reference)' for a in attr_cols}
    }
    
    # Override with some realistic competitors if attributes match
    for comp in competitors:
        comp_dummies = scenario_to_dummies(competitors[comp])
        comp_u = mnl_model.coef_[0].dot(comp_dummies)
        competitors[comp]['_utility'] = comp_u
    
    # Logit probabilities
    all_utils = [your_u] + [c['_utility'] for c in competitors.values()]
    exp_u = np.exp(np.array(all_utils) - max(all_utils))
    probs = exp_u / exp_u.sum()
    
    lines.append(f"\nPredicted Market Shares:")
    lines.append(f"  Your Product:    {probs[0]:.1%}")
    for i, (name, comp) in enumerate(competitors.items(), 1):
        lines.append(f"  {name:15s}: {probs[i]:.1%}")
    
    # Traction computation
    lines.append("\n" + "="*60)
    lines.append("TRACTION = V × A × E")
    lines.append("="*60)
    
    # Auto-detect pillar mapping
    v_attrs = [a for a in attr_cols if any(k in a.lower() for k in ['range', 'smart', 'feature', 'performance'])]
    a_attrs = [a for a in attr_cols if any(k in a.lower() for k in ['price', 'service', 'charge', 'access'])]
    e_attrs = [a for a in attr_cols if any(k in a.lower() for k in ['warranty', 'trust', 'brand', 'evidence'])]
    
    def pillar_score(scenario, attrs):
        if not attrs:
            return 0.5
        score = 0
        for attr in attrs:
            val = scenario.get(attr, '(reference)')
            # Find dummy for this level
            dummy_name = f"d_{attr}_{val}" if val != '(reference)' else None
            if dummy_name and dummy_name in dummy_cols:
                idx = dummy_cols.index(dummy_name)
                score += mnl_model.coef_[0][idx]
        return 1 / (1 + np.exp(-score))  # sigmoid to 0-1
    
    V = pillar_score(scenario, v_attrs)
    A = pillar_score(scenario, a_attrs)
    E = pillar_score(scenario, e_attrs)
    traction = V * A * E
    
    lines.append(f"  V (Value)     : {V:.3f}  [{', '.join(v_attrs) or 'none'}]")
    lines.append(f"  A (Access)    : {A:.3f}  [{', '.join(a_attrs) or 'none'}]")
    lines.append(f"  E (Evidence)  : {E:.3f}  [{', '.join(e_attrs) or 'none'}]")
    lines.append(f"  Traction      : {traction:.3f}")
    
    # CLV
    lines.append("\n" + "="*60)
    lines.append("CLV PROJECTION")
    lines.append("="*60)
    
    market_size = 100000  # default TAM
    margin = 15000
    cac = 5000
    years = 5
    
    share = probs[0]
    clv = share * market_size * margin * years - cac
    
    lines.append(f"  Market Size   : {market_size:,}")
    lines.append(f"  Your Share    : {share:.1%}")
    lines.append(f"  Margin/Unit   : ₹{margin:,}")
    lines.append(f"  CAC           : ₹{cac:,}")
    lines.append(f"  Ownership     : {years} years")
    lines.append(f"  CLV           : ₹{clv:,.0f}")
    
    lines.append("\n✅ Simulation complete.")
    results_html.value = "<pre style='font-family:monospace; font-size:13px; line-height:1.5;'>" + "\n".join(lines) + "</pre>"
    
    render_viz(scenario, probs, V, A, E, traction, competitors)

def on_reset(_):
    scenario_status.value = "<i>Load MNL model first.</i>"
    results_html.value = ""
    viz_panel.children = []

def render_viz(scenario, probs, V, A, E, traction, competitors):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Market share pie/bar
    ax = axes[0]
    names = ['Your Product'] + list(competitors.keys())
    values = list(probs)
    colors = ['#2c7a7b'] + ['#718096', '#d69e2e', '#e53e3e']
    ax.barh(names[::-1], values[::-1], color=colors[:len(names)][::-1], edgecolor='black')
    ax.set_xlabel('Predicted Choice Probability')
    ax.set_title('Market Share Simulation')
    for i, v in enumerate(values[::-1]):
        ax.text(v + 0.01, i, f'{v:.1%}', va='center', fontsize=10)
    
    # Plot 2: Traction pillars
    ax = axes[1]
    pillars = ['V\n(Value)', 'A\n(Access)', 'E\n(Evidence)']
    pvals = [V, A, E]
    pcolors = ['#2c7a7b', '#d69e2e', '#e53e3e']
    bars = ax.bar(pillars, pvals, color=pcolors, edgecolor='black')
    ax.set_ylabel('Score (0-1)')
    ax.set_title(f'Traction = {traction:.3f}')
    ax.set_ylim(0, 1.05)
    for bar, val in zip(bars, pvals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
               f'{val:.2f}', ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    questions = """
    <div style="background:#fffbeb; border:2px dashed #f59e0b; border-radius:12px; padding:16px; margin:12px 0;">
    <h4 style="margin-top:0; color:#b45309;">Discussion Questions</h4>
    <ol style="color:#78350f;">
    <li><b>Share:</b> Is your predicted share above 20%? If not, which competitor are you losing to?</li>
    <li><b>Traction:</b> Which pillar is lowest? Is it V, A, or E? That is your strategic bottleneck.</li>
    <li><b>Tradeoff:</b> What happens to share if you cut price by 25K but keep everything else?</li>
    <li><b>CLV:</b> Does the configuration with highest share also have highest CLV? If not, why?</li>
    </ol>
    </div>
    """
    viz_panel.children = [widgets.HTML(questions)]

# =============================================================================
# WIRE & ASSEMBLE
# =============================================================================

btn_source.on_click(on_source)
btn_add_scenario.on_click(add_scenario_row)
btn_simulate.on_click(on_simulate)
btn_reset.on_click(on_reset)

full_ui = widgets.VBox([
    source_panel,
    scenario_container,
    results_panel,
    viz_panel
])

display(full_ui)
