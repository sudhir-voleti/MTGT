# -*- coding: utf-8 -*-
"""
Lec09 — Step 6c: V×A×E Overlay on Simulator Results
Shows V/A/E decomposition for each simulated product configuration.
Pure code cell. Run AFTER a simulation in 05b_simulator.py.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/06c_vae_overlay.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import ipywidgets as widgets

# =============================================================================
# 1. Check prerequisites
# =============================================================================

missing = []
if 'sim_df' not in globals():
    missing.append("sim_df (run simulator first)")
if 'vae_df' not in globals():
    missing.append("vae_df (run VAE mapper first)")
if 'vae_mapping' not in globals() and 'vae_df' not in globals():
    missing.append("vae_mapping (run VAE mapper first)")

if missing:
    print("⚠ Missing prerequisites:")
    for m in missing:
        print(f"   • {m}")
    print("\nPlease run 05b_simulator.py and 06b_vae_mapper.py first.")
    raise SystemExit("Prerequisites missing")

# Reconstruct mapping from vae_df if not in globals
if 'vae_mapping' in globals():
    vae_map = globals()['vae_mapping']
else:
    # Try to infer from 06b state if available
    vae_map = None

sim_df = globals()['sim_df']

# =============================================================================
# 2. Expectation + Run Overlay button
# =============================================================================

print("="*60)
print("V × A × E OVERLAY ON SIMULATOR RESULTS")
print("="*60)
print("\nThis will decompose each product's predicted share into:")
print("   V (Value) — performance attributes")
print("   A (Access) — friction-reducing attributes")  
print("   E (Evidence) — trust-building attributes")
print("\nYou need the product configurations from your last simulation.")
print()

run_btn = widgets.Button(
    description="▶ Run VAE Overlay",
    button_style='primary',
    layout=widgets.Layout(width='200px', height='40px')
)
run_btn.on_click(lambda b: run_overlay())
display(run_btn)

# =============================================================================
# 3. Main overlay
# =============================================================================

def run_overlay():
    clear_output(wait=True)
    print("="*60)
    print("V × A × E DECOMPOSITION")
    print("="*60)

    # We need the product configs from the last simulation
    # Since they're not stored globally, we can't reconstruct them perfectly
    # Instead, we'll show a message explaining the limitation
    # and compute V/A/E for the *share* that was projected

    print("\n📋 Note: This overlay shows the V/A/E composition of the")
    print("   *respondent population* that chose each product, not the product itself.")
    print("   It answers: 'What kind of buyers chose Product X?'")
    print()

    # For each product, find respondents who chose it and show their mean V/A/E
    product_cols = [c for c in sim_df.columns if c.startswith('P_') and c != 'P_None']

    if 'vae_df' in globals():
        vae = globals()['vae_df']
        merged = sim_df.merge(vae[['RespID', 'V', 'A', 'E']], on='RespID', how='left')

        # Weighted average V/A/E by choice probability for each product
        print("\n" + "="*60)
        print("WEIGHTED V/A/E BY PRODUCT")
        print("="*60)
        print("   (Weighted by choice probability — higher probability = more weight)")

        vae_by_product = []
        for pc in product_cols:
            prod_name = pc.replace('P_', '')
            weights = merged[pc].values
            if weights.sum() > 0:
                v_wt = np.average(merged['V'].fillna(0), weights=weights)
                a_wt = np.average(merged['A'].fillna(0), weights=weights)
                e_wt = np.average(merged['E'].fillna(0), weights=weights)
                vae_by_product.append({
                    'Product': prod_name,
                    'V (Value)': v_wt,
                    'A (Access)': a_wt,
                    'E (Evidence)': e_wt,
                    'Traction': v_wt * a_wt * e_wt
                })

        vae_prod_df = pd.DataFrame(vae_by_product)
        print(vae_prod_df.round(2).to_string(index=False))

        # Stacked bar chart
        fig, ax = plt.subplots(figsize=(9, 5.5))
        products = vae_prod_df['Product'].tolist()
        v_vals = vae_prod_df['V (Value)'].values
        a_vals = vae_prod_df['A (Access)'].values
        e_vals = vae_prod_df['E (Evidence)'].values

        x = np.arange(len(products))
        width = 0.6

        ax.bar(x, v_vals, width, label='V (Value)', color='#E37222', edgecolor='white')
        ax.bar(x, a_vals, width, bottom=v_vals, label='A (Access)', color='#003366', edgecolor='white')
        ax.bar(x, e_vals, width, bottom=v_vals + a_vals, label='E (Evidence)', color='#64748b', edgecolor='white')

        ax.set_ylabel('Composite Score', fontsize=12)
        ax.set_title('V × A × E Decomposition by Product', fontsize=13, color='#003366')
        ax.set_xticks(x)
        ax.set_xticklabels(products)
        ax.legend(loc='upper right')
        plt.tight_layout()
        plt.show()

        # Traction score bar chart
        fig, ax = plt.subplots(figsize=(7, 4))
        traction = vae_prod_df['Traction'].values
        colors = ['#E37222' if 'Yana' in p else '#003366' for p in products]
        ax.bar(products, traction, color=colors, edgecolor='white')
        ax.set_ylabel('Traction Score (V × A × E)', fontsize=12)
        ax.set_title('Traction Score by Product', fontsize=13, color='#003366')
        for i, v in enumerate(traction):
            ax.text(i, v + max(traction)*0.02, f'{v:.1f}', ha='center', fontsize=11)
        plt.tight_layout()
        plt.show()

    # -------------------------------------------------------------------------
    # Segment VAE for None choosers
    # -------------------------------------------------------------------------

    if 'Segment' in sim_df.columns and 'vae_df' in globals():
        print("\n" + "="*60)
        print("V/A/E OF 'NONE' CHOOSERS BY SEGMENT")
        print("="*60)

        merged_seg = sim_df.merge(vae[['RespID', 'V', 'A', 'E', 'Segment']], on='RespID', how='left')
        none_weights = merged_seg['P_None'].values

        for seg in sorted(merged_seg['Segment'].unique()):
            seg_data = merged_seg[merged_seg['Segment'] == seg]
            weights = seg_data['P_None'].values
            if weights.sum() > 0:
                v_wt = np.average(seg_data['V'].fillna(0), weights=weights)
                a_wt = np.average(seg_data['A'].fillna(0), weights=weights)
                e_wt = np.average(seg_data['E'].fillna(0), weights=weights)
                print(f"\n{seg}:")
                print(f"   V (Value):    {v_wt:6.2f}")
                print(f"   A (Access):   {a_wt:6.2f}")
                print(f"   E (Evidence): {e_wt:6.2f}")
                print(f"   → Why they chose None: {'Low A (price too high)' if a_wt < 0 else 'Low E (no trust)' if e_wt < 0 else 'Low V (product not compelling)'}")

    # -------------------------------------------------------------------------
    # Scribble pause
    # -------------------------------------------------------------------------

    html_content = """
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
        <h3>Pause and Reflect: Which Pillar Is Your Weakness?</h3>
        <p>Look at the stacked bar chart. For your Yana product, which pillar is the shortest? That is your strategic gap.</p>
        <table class="scribble-table">
          <thead>
            <tr><th>Product</th><th>Weakest Pillar</th><th>Fix It By...</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>Yana (my product)</td>
              <td><textarea placeholder="e.g., E — not enough trust..."></textarea></td>
              <td><textarea placeholder="e.g., Longer warranty or Honda partnership..."></textarea></td>
            </tr>
            <tr>
              <td>Competitor A</td>
              <td><textarea placeholder="..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
            </tr>
            <tr>
              <td>Competitor B</td>
              <td><textarea placeholder="..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top:12px;"><strong>Insight:</strong> You do not need to win on all three pillars. You need to win on the pillar that matters most to your target segment, and be <em>good enough</em> on the other two. The Traction score tells you where "good enough" is not enough.</p>
      </div>
    </div>
    """
    display(HTML(html_content))
