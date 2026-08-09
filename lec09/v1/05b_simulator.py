# -*- coding: utf-8 -*-
"""
Lec09 — Step 5b: Market Simulator (Generic)
Interactive product configurator + 'Simulate Market' button.
Pure code cell. Run AFTER 05a_theory.py in a separate Colab cell.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/05b_simulator.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

_state = {'ib_df': None, 'attr_map': None}

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
        show_configurator()
    upload_widget.observe(on_upload, names='value')
    display(upload_widget)

# =============================================================================
# 2. Parse dummy columns to reconstruct attribute levels
# =============================================================================

def parse_attributes(ib_df):
    """Parse dummy column names like d_Range_110km into attribute-level mapping."""
    pw_cols = [c for c in ib_df.columns if c not in ['RespID', 'Segment', 'Intercept', 'Cluster']]

    attr_map = {}
    for col in pw_cols:
        if not col.startswith('d_'):
            continue
        parts = col.split('_', 2)
        if len(parts) < 3:
            continue
        attr = parts[1]
        level = parts[2]
        attr_map.setdefault(attr, {'dummies': [], 'reference': None})
        attr_map[attr]['dummies'].append({'col': col, 'level': level})

    # Infer reference level: we need to know all possible levels.
    # Since we only have dummies for non-reference levels, we can't know the reference name
    # from ib_df alone. We'll use the dummy level names and add a "Reference" option.
    for attr in attr_map:
        levels = [d['level'] for d in attr_map[attr]['dummies']]
        attr_map[attr]['levels'] = levels
        attr_map[attr]['all_levels'] = levels + ['Reference (baseline)']

    return attr_map

# =============================================================================
# 3. Build product configurator
# =============================================================================

def show_configurator():
    ib_df = _state['ib_df']
    attr_map = parse_attributes(ib_df)
    _state['attr_map'] = attr_map

    attrs = list(attr_map.keys())

    clear_output(wait=True)
    print("="*60)
    print("MARKET SIMULATOR: CONFIGURE YOUR PRODUCTS")
    print("="*60)
    print("\nSet the attribute levels for each product in the competitive set.")
    print("The simulator will compute choice probabilities using each respondent's part-worths.")
    print()

    # Build dropdowns for each product
    products = [
        ('Product 1: Your Product (Yana)', 'Yana'),
        ('Product 2: Competitor A', 'Comp A'),
        ('Product 3: Competitor B', 'Comp B'),
    ]

    product_widgets = {}

    for prod_label, prod_key in products:
        print(f"\n{prod_label}")
        attr_dropdowns = {}
        row_widgets = []
        for attr in attrs:
            levels = attr_map[attr]['all_levels']
            dd = widgets.Dropdown(
                options=levels,
                value=levels[0],
                description=f'{attr}:',
                layout=widgets.Layout(width='220px'),
                style={'description_width': '70px'}
            )
            attr_dropdowns[attr] = dd
            row_widgets.append(dd)

        # Display in rows of 4
        for i in range(0, len(row_widgets), 4):
            display(widgets.HBox(row_widgets[i:i+4]))

        product_widgets[prod_key] = attr_dropdowns

    # None utility
    none_util = widgets.FloatSlider(
        value=0.0,
        min=-3.0,
        max=1.0,
        step=0.1,
        description='None utility:',
        layout=widgets.Layout(width='400px'),
        style={'description_width': '100px'}
    )
    print("\n'None of these' option utility (0 = neutral, negative = less attractive):")
    display(none_util)

    # Store
    _state['product_widgets'] = product_widgets
    _state['none_util'] = none_util

    # Expectation + Simulate button
    print("\n" + "-"*60)
    print("📋 What will happen when you click 'Simulate Market':")
    print("   • Compute utility for each product using every respondent's part-worths")
    print("   • Apply logit choice rule: P = exp(U) / sum(exp(all U))")
    print("   • Average across 400 respondents → market share projection")
    print("   • Show overall share + segment-specific shares (if available)")
    print("   • Estimated runtime: ~3 seconds")
    print()

    sim_btn = widgets.Button(
        description="▶ Simulate Market",
        button_style='primary',
        layout=widgets.Layout(width='200px', height='40px')
    )
    sim_btn.on_click(lambda b: run_simulation())
    display(sim_btn)

# =============================================================================
# 4. Run simulation
# =============================================================================

def run_simulation():
    ib_df = _state['ib_df']
    attr_map = _state['attr_map']
    product_widgets = _state['product_widgets']
    none_util = _state['none_util'].value

    clear_output(wait=True)
    print("="*60)
    print("MARKET SIMULATION RESULTS")
    print("="*60)

    # Build product configurations
    products = []
    for prod_key in ['Yana', 'Comp A', 'Comp B']:
        config = {}
        for attr, dd in product_widgets[prod_key].items():
            config[attr] = dd.value
        products.append({'name': prod_key, 'config': config})

    # Show configurations
    print("\n📦 Configured Products:")
    for p in products:
        cfg_str = ', '.join([f"{k}={v}" for k, v in p['config'].items()])
        print(f"   {p['name']}: {cfg_str}")
    print(f"   None of these: utility = {none_util:.1f}")

    # -------------------------------------------------------------------------
    # Compute utilities per respondent
    # -------------------------------------------------------------------------

    pw_cols = [c for c in ib_df.columns if c not in ['RespID', 'Segment', 'Intercept', 'Cluster']]

    results = []
    for _, resp in ib_df.iterrows():
        utilities = []
        for prod in products:
            u = 0.0
            for attr, level in prod['config'].items():
                if level == 'Reference (baseline)':
                    u += 0.0
                else:
                    dummy_col = f'd_{attr}_{level}'
                    if dummy_col in resp:
                        u += float(resp[dummy_col]) if pd.notna(resp[dummy_col]) else 0.0
            utilities.append(u)

        # Add None
        utilities.append(none_util)

        # Logit probabilities
        max_u = max(utilities)
        exp_u = np.exp(np.array(utilities) - max_u)  # numerical stability
        probs = exp_u / exp_u.sum()

        row = {'RespID': resp['RespID']}
        if 'Segment' in resp:
            row['Segment'] = resp['Segment']
        for i, prod in enumerate(products):
            row[f'P_{prod["name"]}'] = probs[i]
        row['P_None'] = probs[-1]
        results.append(row)

    sim_df = pd.DataFrame(results)

    # -------------------------------------------------------------------------
    # Overall shares
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("PREDICTED MARKET SHARES")
    print("="*60)

    share_cols = [c for c in sim_df.columns if c.startswith('P_')]
    overall = sim_df[share_cols].mean() * 100

    share_table = pd.DataFrame({
        'Product': [c.replace('P_', '') for c in share_cols],
        'Share (%)': overall.round(1).values
    })
    print(share_table.to_string(index=False))

    # Bar chart
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = ['#E37222' if 'Yana' in name else '#003366' for name in share_table['Product']]
    colors[-1] = '#64748b'  # None is gray
    bars = ax.barh(share_table['Product'], share_table['Share (%)'], color=colors, edgecolor='white')
    ax.set_xlabel('Market Share (%)', fontsize=12)
    ax.set_title('Predicted Market Share', fontsize=13, color='#003366')
    for bar, val in zip(bars, share_table['Share (%)']):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f}%', va='center', fontsize=11)
    plt.tight_layout()
    plt.show()

    # -------------------------------------------------------------------------
    # Segment-specific shares
    # -------------------------------------------------------------------------

    if 'Segment' in sim_df.columns:
        print("\n" + "="*60)
        print("SEGMENT-SPECIFIC SHARES")
        print("="*60)

        seg_shares = sim_df.groupby('Segment')[share_cols].mean() * 100
        print(seg_shares.round(1))

        # Grouped bar chart
        fig, ax = plt.subplots(figsize=(9, 5))
        x = np.arange(len(share_cols))
        width = 0.25
        segments = sorted(sim_df['Segment'].unique())
        seg_colors = ['#E37222', '#003366', '#64748b'][:len(segments)]

        for i, seg in enumerate(segments):
            vals = seg_shares.loc[seg].values
            ax.bar(x + i*width, vals, width, label=seg, color=seg_colors[i], edgecolor='white')

        ax.set_ylabel('Share (%)', fontsize=12)
        ax.set_title('Market Share by Segment', fontsize=13, color='#003366')
        ax.set_xticks(x + width)
        ax.set_xticklabels([c.replace('P_', '') for c in share_cols], rotation=15, ha='right')
        ax.legend(title='Segment')
        plt.tight_layout()
        plt.show()

    # Store
    globals()['sim_df'] = sim_df

    # -------------------------------------------------------------------------
    # Scribble pause
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
        <h3>Pause and Reflect: Did Your Strategy Work?</h3>
        <p>Look at the predicted shares above. How did your configuration perform?</p>
        <table class="scribble-table">
          <thead>
            <tr><th>Question</th><th>My Answer</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>Did Yana win the segment I was targeting?</td>
              <td><textarea placeholder="Yes / No / Partially — explain..."></textarea></td>
            </tr>
            <tr>
              <td>Which competitor is my biggest threat?</td>
              <td><textarea placeholder="e.g., Honda because of brand equity..."></textarea></td>
            </tr>
            <tr>
              <td>What is the ONE attribute I should change to improve share?</td>
              <td><textarea placeholder="e.g., Drop price to 85K, or switch to Honda brand..."></textarea></td>
            </tr>
            <tr>
              <td>What is the trade-off? (What do I sacrifice by making that change?)</td>
              <td><textarea placeholder="e.g., Lower margin, or lose Tech segment..."></textarea></td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top:12px;"><strong>Insight:</strong> Market share is not about building the best product. It is about building the product that <em>wins the target segment</em> while accepting that other segments will prefer competitors. Strategy is choosing whom to delight and whom to disappoint.</p>
        <p><strong>Next:</strong> Reconfigure your product and re-run the simulation. Iterate until you find the configuration that maximizes share for your target segment. Then use that insight to design your marketing campaign.</p>
      </div>
    </div>
    """))

    # Show re-configure button
    print("\n" + "-"*60)
    print("Want to try a different configuration? Re-run this cell to adjust products.")
    print("-"*60)

if proceed:
    show_configurator()
