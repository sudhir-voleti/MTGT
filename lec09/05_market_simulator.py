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
    
    # Ensure dummy_name is string
    coef_df['dummy_name'] = coef_df['dummy_name'].astype(str)
    
    # Parse coefficients
    dummy_rows = coef_df[coef_df['dummy_name'].str.startswith('d_')]
    intercept_row = coef_df[coef_df['dummy_name'].str.lower() == 'intercept']
  
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
    # Force button state update
    btn_sim.disabled = True
    btn_sim.disabled = False  

def build_config_ui():
    global _config_selectors
    _config_selectors = []
    
    selectors = []
    for attr, levels in sorted(attr_levels.items()):
        dd = widgets.Dropdown(options=levels, value=levels[0], description=f'{attr}:', 
                              layout=widgets.Layout(width='240px'))
        selectors.append(dd)
        _config_selectors.append(dd)
    
    rows = []
    for i in range(0, len(selectors), 3):
        row = widgets.HBox(selectors[i:i+3])
        rows.append(row)
    
    config_panel.children = [
        widgets.HTML("<h3>Step 2 — Configure Your Product</h3>"),
        widgets.HTML("<p>Select attribute levels. Reference = worst level.</p>"),
        widgets.VBox(rows),
        widgets.HBox([btn_sim, sim_status])
    ]

def compute_utility(scenario):
    """Compute utility for a given attribute configuration."""
    d = np.zeros(len(dummy_cols))
    for i, dummy in enumerate(dummy_cols):
        parts = dummy[2:].split('_')
        attr = parts[0]
        level = '_'.join(parts[1:])
        if scenario.get(attr) == level:
            d[i] = 1
    return mnl_model.coef_[0].dot(d) + mnl_model.intercept_

def pillar_score(scenario, attrs):
    """Compute pillar score (sigmoid of sum of part-worths)."""
    if not attrs:
        return 0.5
    score = 0
    for attr in attrs:
        val = scenario.get(attr, '(reference)')
        dummy_name = f"d_{attr}_{val}"
        if dummy_name in dummy_cols:
            idx = dummy_cols.index(dummy_name)
            score += mnl_model.coef_[0][idx]
    return 1 / (1 + np.exp(-score))

def on_sim(_):
    with out:
        clear_output()
        
        # Read your product config
        your_config = {}
        for attr, dd in _config_selectors.items():
            your_config[attr] = dd.value
        
        # Competitor config (hardcoded realistic default, editable later if needed)
        competitor_config = {
            'Range': '110km',
            'Charge': '1.5hrs', 
            'Price': '95K',
            'Service': '300cities',
            'Smart': 'Advanced',
            'Warranty': '3yr'
        }
        # Fill missing attrs with reference
        for attr in attr_levels:
            if attr not in competitor_config:
                competitor_config[attr] = '(reference)'
        
        # Compute utilities
        your_u = compute_utility(your_config)
        comp_u = compute_utility(competitor_config)
        none_u = 0.0  # outside good
        
        # Logit choice probabilities
        utils = [your_u, comp_u, none_u]
        exp_u = np.exp(np.array(utils) - max(utils))
        probs = exp_u / exp_u.sum()
        
        print("="*60)
        print("MARKET SIMULATION")
        print("="*60)
        
        print(f"\nYour Product:")
        for attr, val in sorted(your_config.items()):
            print(f"  {attr:15s}: {val}")
        print(f"  Utility: {your_u:.3f}")
        
        print(f"\nCompetitor:")
        for attr, val in sorted(competitor_config.items()):
            print(f"  {attr:15s}: {val}")
        print(f"  Utility: {comp_u:.3f}")
        
        print(f"\nPredicted Choice Probabilities:")
        print(f"  Your Product:  {probs[0]:.1%}")
        print(f"  Competitor:    {probs[1]:.1%}")
        print(f"  None:          {probs[2]:.1%}")
        
        # Traction
        print(f"\n{'='*60}")
        print("TRACTION = V × A × E")
        print("="*60)
        
        v_attrs = [a for a in attr_levels if any(k in a.lower() for k in ['range', 'smart', 'feature'])]
        a_attrs = [a for a in attr_levels if any(k in a.lower() for k in ['price', 'service', 'charge'])]
        e_attrs = [a for a in attr_levels if any(k in a.lower() for k in ['warranty', 'trust'])]
        
        V = pillar_score(your_config, v_attrs)
        A = pillar_score(your_config, a_attrs)
        E = pillar_score(your_config, e_attrs)
        traction = V * A * E
        
        print(f"  V (Value):     {V:.3f}")
        print(f"  A (Access):    {A:.3f}")
        print(f"  E (Evidence):  {E:.3f}")
        print(f"  Traction:      {traction:.3f}")
        
        # CLV
        share = probs[0]
        clv = share * 100000 * 15000 * 5 - 5000
        print(f"\n{'='*60}")
        print("CLV PROJECTION")
        print("="*60)
        print(f"  Market Share:  {share:.1%}")
        print(f"  CLV:           ₹{clv:,.0f}")
        
        # Plot
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        
        # Share bars
        ax = axes[0]
        names = ['Your Product', 'Competitor', 'None']
        vals = probs
        colors = ['#2c7a7b', '#718096', '#e53e3e']
        bars = ax.barh(names, vals, color=colors, edgecolor='black')
        ax.set_xlabel('Choice Probability')
        ax.set_title('Predicted Market Shares')
        ax.set_xlim(0, 1)
        for i, (bar, v) in enumerate(zip(bars, vals)):
            ax.text(v + 0.02, bar.get_y() + bar.get_height()/2, f'{v:.1%}', 
                   va='center', fontsize=11, fontweight='bold')
        
        # Traction pillars
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
