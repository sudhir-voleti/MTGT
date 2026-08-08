# ═══════════════════════════════════════════════════════════════════
#  STEP 5: Market Simulator — Simple Slider-Based Configurator
# ═══════════════════════════════════════════════════════════════════

import io
import numpy as np
import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from google.colab import files

# =============================================================================
# STATE
# =============================================================================

mnl_model = None
dummy_cols = []
attr_levels = {}  # attr -> [reference, level1, level2, ...]

# =============================================================================
# WIDGETS
# =============================================================================

# --- Source ---
upload_mnl = widgets.FileUpload(accept='.csv', multiple=False, description='📁 MNL Coeffs', 
                                button_style='primary', layout=widgets.Layout(width='280px'))
btn_load = widgets.Button(description='▶ Load', button_style='success')
source_status = widgets.HTML("Upload MNL coefficients CSV from Step 4.")

source_panel = widgets.VBox([
    widgets.HTML("<h2>Market Simulator: Step 1 — Load MNL Model</h2>"),
    widgets.HBox([upload_mnl, btn_load]),
    source_status
])

# --- Config panel (populated after load) ---
config_status = widgets.HTML("<i>Load MNL coefficients first.</i>")
config_panel = widgets.VBox([])

# --- Competitor panel ---
comp_price = widgets.Dropdown(options=['85K', '110K', '140K'], value='110K', description='Comp Price:')
comp_service = widgets.Dropdown(options=['25cities', '100cities', '300cities'], value='300cities', description='Comp Service:')
comp_btn = widgets.Button(description='Set Competitors', button_style='info')

comp_panel = widgets.VBox([
    widgets.HTML("<h4>Competitor Defaults</h4>"),
    widgets.HBox([comp_price, comp_service]),
    comp_btn
])

# --- Simulate ---
btn_sim = widgets.Button(description='▶ Simulate', button_style='success', disabled=True)
sim_status = widgets.HTML("")

# --- Results ---
results_html = widgets.HTML("")
viz_panel = widgets.VBox([])

# =============================================================================
# EVENT HANDLERS
# =============================================================================

def on_load(_):
    global mnl_model, dummy_cols, attr_levels
    
    if not upload_mnl.value:
        source_status.value = "<span style='color:#c53030'>❌ Upload CSV first.</span>"
        return
    
    raw = list(upload_mnl.value.values())[0]['content']
    coef_df = pd.read_csv(io.BytesIO(raw))
    
    # Parse coefficients
    valid = coef_df[coef_df['dummy_name'].apply(lambda x: isinstance(x, str))]
    dummy_rows = valid[valid['dummy_name'].str.startswith('d_')]
    intercept_row = valid[valid['dummy_name'].str.lower() == 'intercept']
    
    dummy_cols = dummy_rows['dummy_name'].tolist()
    coefs = dummy_rows['coefficient'].values
    intercept = intercept_row['coefficient'].values[0] if len(intercept_row) > 0 else 0
    
    # Build simple model
    class SimpleModel:
        def __init__(self, c, inter):
            self.coef_ = np.array([c])
            self.intercept_ = inter
    mnl_model = SimpleModel(coefs, intercept)
    
    # Extract attribute levels from dummy names
    attr_levels = {}
    for d in dummy_cols:
        parts = d[2:].split('_')
        attr = parts[0]
        level = '_'.join(parts[1:])
        if attr not in attr_levels:
            attr_levels[attr] = ['(reference)']
        attr_levels[attr].append(level)
    
    source_status.value = f"✅ Loaded: {len(dummy_cols)} dummies, {len(attr_levels)} attributes, intercept={intercept:.3f}"
    
    # Build config UI
    build_config_ui()
    btn_sim.disabled = False

def build_config_ui():
    selectors = []
    for attr, levels in sorted(attr_levels.items()):
        dd = widgets.Dropdown(options=levels, value=levels[0], description=f'{attr}:', 
                              layout=widgets.Layout(width='240px'))
        selectors.append(dd)
    
    config_panel.children = [
        widgets.HTML("<h3>Step 2 — Configure Your Product</h3>"),
        widgets.HTML("<p>Select attribute levels for your product. Reference = worst level.</p>"),
        widgets.HBox(selectors[:3]) if len(selectors) >= 3 else widgets.HBox(selectors),
        widgets.HBox(selectors[3:6]) if len(selectors) > 3 else widgets.HTML(""),
        widgets.HBox(selectors[6:]) if len(selectors) > 6 else widgets.HTML(""),
        widgets.HBox([btn_sim, sim_status])
    ]
    
    # Store selectors for later
    config_panel._selectors = selectors

def compute_utility(scenario):
    d = np.zeros(len(dummy_cols))
    for i, dummy in enumerate(dummy_cols):
        parts = dummy[2:].split('_')
        attr = parts[0]
        level = '_'.join(parts[1:])
        if attr in scenario and scenario[attr] == level:
            d[i] = 1
    return mnl_model.coef_[0].dot(d) + mnl_model.intercept_

def on_sim(_):
    # Gather current selections
    scenario = {}
    for sel in config_panel._selectors:
        attr = sel.description.replace(':', '')
        scenario[attr] = sel.value
    
    # Competitor (simple: one generic competitor)
    comp = {
        'Price': comp_price.value,
        'Service': comp_service.value
    }
    # Fill other attrs with reference
    for attr in attr_levels:
        if attr not in comp:
            comp[attr] = '(reference)'
    
    # Compute utilities
    your_u = compute_utility(scenario)
    comp_u = compute_utility(comp)
    none_u = 0  # reference
    
    # Logit
    utils = [your_u, comp_u, none_u]
    exp_u = np.exp(np.array(utils) - max(utils))
    probs = exp_u / exp_u.sum()
    
    # Traction
    v_attrs = [a for a in attr_levels if any(k in a.lower() for k in ['range', 'smart', 'feature'])]
    a_attrs = [a for a in attr_levels if any(k in a.lower() for k in ['price', 'service', 'charge'])]
    e_attrs = [a for a in attr_levels if any(k in a.lower() for k in ['warranty', 'trust'])]
    
    def pillar_score(scen, attrs):
        if not attrs:
            return 0.5
        score = sum([mnl_model.coef_[0][dummy_cols.index(f"d_{a}_{scen[a]}")] 
                     for a in attrs if f"d_{a}_{scen[a]}" in dummy_cols])
        return 1 / (1 + np.exp(-score))
    
    V = pillar_score(scenario, v_attrs)
    A = pillar_score(scenario, a_attrs)
    E = pillar_score(scenario, e_attrs)
    traction = V * A * E
    
    # CLV
    share = probs[0]
    clv = share * 100000 * 15000 * 5 - 5000
    
    # Display
    lines = []
    lines.append("="*60)
    lines.append("MARKET SIMULATION RESULTS")
    lines.append("="*60)
    lines.append(f"\nYour Product: {scenario}")
    lines.append(f"Competitor:   {comp}")
    lines.append(f"\nPredicted Shares:")
    lines.append(f"  Your Product:  {probs[0]:.1%}")
    lines.append(f"  Competitor:    {probs[1]:.1%}")
    lines.append(f"  None:          {probs[2]:.1%}")
    lines.append(f"\nTraction = V × A × E:")
    lines.append(f"  V (Value):     {V:.3f}")
    lines.append(f"  A (Access):    {A:.3f}")
    lines.append(f"  E (Evidence):  {E:.3f}")
    lines.append(f"  Traction:      {traction:.3f}")
    lines.append(f"\nCLV Projection:")
    lines.append(f"  Market Share:  {share:.1%}")
    lines.append(f"  CLV:           ₹{clv:,.0f}")
    
    results_html.value = "<pre style='font-family:monospace; font-size:13px;'>" + "\n".join(lines) + "</pre>"
    
    # Viz
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    
    ax = axes[0]
    names = ['Your Product', 'Competitor', 'None']
    vals = probs
    colors = ['#2c7a7b', '#718096', '#e53e3e']
    ax.barh(names, vals, color=colors, edgecolor='black')
    ax.set_xlabel('Choice Probability')
    ax.set_title('Predicted Market Shares')
    for i, v in enumerate(vals):
        ax.text(v + 0.01, i, f'{v:.1%}', va='center')
    
    ax = axes[1]
    pillars = ['V\n(Value)', 'A\n(Access)', 'E\n(Evidence)']
    pvals = [V, A, E]
    pcolors = ['#2c7a7b', '#d69e2e', '#e53e3e']
    bars = ax.bar(pillars, pvals, color=pcolors, edgecolor='black')
    ax.set_ylabel('Score')
    ax.set_title(f'Traction = {traction:.3f}')
    ax.set_ylim(0, 1.05)
    for bar, val in zip(bars, pvals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{val:.2f}', ha='center')
    
    plt.tight_layout()
    plt.show()
    
    questions = """
    <div style="background:#fffbeb; border:2px dashed #f59e0b; border-radius:12px; padding:16px; margin:12px 0;">
    <h4 style="margin-top:0; color:#b45309;">Discussion Questions</h4>
    <ol style="color:#78350f;">
    <li><b>Share:</b> Is your share above 25%? If not, which attribute is killing you?</li>
    <li><b>Traction:</b> Which pillar is lowest? That is your bottleneck.</li>
    <li><b>Tradeoff:</b> Change one slider. What happens to share and traction?</li>
    <li><b>CLV:</b> Does highest share = highest CLV? When does it not?</li>
    </ol>
    </div>
    """
    viz_panel.children = [widgets.HTML(questions)]

# =============================================================================
# WIRE
# =============================================================================

btn_load.on_click(on_load)
btn_sim.on_click(on_sim)

full_ui = widgets.VBox([
    source_panel,
    config_panel,
    comp_panel,
    results_html,
    viz_panel
])

display(full_ui)
