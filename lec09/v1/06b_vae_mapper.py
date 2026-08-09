# -*- coding: utf-8 -*-
"""
Lec09 — Step 6b: V×A×E Mapper + Traction Landscape Scatterplot
Interactive attribute-to-pillar mapping. Pure code cell.
Run AFTER 06a_vae_theory.py in a separate Colab cell.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/06b_vae_mapper.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import ipywidgets as widgets

_state = {'ib_df': None, 'mapping': None, 'vae_scores': None}

# =============================================================================
# 1. Retrieve ib_df
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
        show_mapping_ui()
    upload_widget.observe(on_upload, names='value')
    display(upload_widget)

# =============================================================================
# 2. Parse attributes from dummy columns
# =============================================================================

def parse_attributes(ib_df):
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
        attr_map.setdefault(attr, {'cols': []})
        attr_map[attr]['cols'].append(col)
    return attr_map

# =============================================================================
# 3. Mapping UI
# =============================================================================

def show_mapping_ui():
    ib_df = _state['ib_df']
    attr_map = parse_attributes(ib_df)
    _state['attr_map'] = attr_map
    attrs = list(attr_map.keys())

    clear_output(wait=True)
    print("="*60)
    print("V × A × E ATTRIBUTE MAPPING")
    print("="*60)
    print("\nMap each attribute to a Traction pillar.")
    print("This is your strategic choice — there is no single right answer.")
    print()

    # Default guesses based on attribute names
    def guess_pillar(attr_name):
        an = attr_name.lower()
        if any(k in an for k in ['range', 'smart', 'power', 'speed', 'perf']):
            return 'V (Value)'
        elif any(k in an for k in ['price', 'service', 'charge', 'time', 'cost', 'avail']):
            return 'A (Access)'
        elif any(k in an for k in ['warranty', 'brand', 'trust', 'review', 'cert']):
            return 'E (Evidence)'
        else:
            return 'Exclude'

    pillar_options = ['V (Value)', 'A (Access)', 'E (Evidence)', 'Exclude']
    mapping_widgets = {}
    rows = []

    for attr in attrs:
        default = guess_pillar(attr)
        dd = widgets.Dropdown(
            options=pillar_options,
            value=default,
            description=f'{attr}:',
            layout=widgets.Layout(width='280px'),
            style={'description_width': '100px'}
        )
        mapping_widgets[attr] = dd
        rows.append(dd)

    for i in range(0, len(rows), 3):
        display(widgets.HBox(rows[i:i+3]))

    print("\n" + "-"*60)
    print("📋 What will happen when you click 'Compute Traction':")
    print("   • Sum part-worths per respondent for each pillar")
    print("   • Plot V vs. A scatterplot (colored by segment)")
    print("   • Show mean V/A/E by segment")
    print("   • Estimated runtime: ~3 seconds")
    print()

    btn_row = widgets.HBox([
        widgets.Button(description="▶ Compute Traction", button_style='primary', layout=widgets.Layout(width='200px', height='40px')),
        widgets.Button(description="↺ Reset Mapping", button_style='warning', layout=widgets.Layout(width='180px', height='40px', margin='0 0 0 10px'))
    ])

    def on_compute(b):
        mapping = {attr: mapping_widgets[attr].value for attr in attrs}
        _state['mapping'] = mapping
        compute_and_plot()

    def on_reset(b):
        show_mapping_ui()

    btn_row.children[0].on_click(on_compute)
    btn_row.children[1].on_click(on_reset)
    display(btn_row)

# =============================================================================
# 4. Compute and plot
# =============================================================================

def compute_and_plot():
    ib_df = _state['ib_df']
    attr_map = _state['attr_map']
    mapping = _state['mapping']

    clear_output(wait=True)
    print("="*60)
    print("TRACTION LANDSCAPE")
    print("="*60)

    # Compute V, A, E per respondent
    v_cols = []
    a_cols = []
    e_cols = []

    for attr, info in attr_map.items():
        pillar = mapping[attr]
        if pillar == 'V (Value)':
            v_cols.extend(info['cols'])
        elif pillar == 'A (Access)':
            a_cols.extend(info['cols'])
        elif pillar == 'E (Evidence)':
            e_cols.extend(info['cols'])

    v_scores = ib_df[v_cols].sum(axis=1) if v_cols else pd.Series(0, index=ib_df.index)
    a_scores = ib_df[a_cols].sum(axis=1) if a_cols else pd.Series(0, index=ib_df.index)
    e_scores = ib_df[e_cols].sum(axis=1) if e_cols else pd.Series(0, index=ib_df.index)

    vae_df = pd.DataFrame({
        'RespID': ib_df['RespID'],
        'V': v_scores.values,
        'A': a_scores.values,
        'E': e_scores.values
    })
    if 'Segment' in ib_df.columns:
        vae_df['Segment'] = ib_df['Segment'].values

    _state['vae_scores'] = vae_df
    globals()['vae_df'] = vae_df

    # Show mapping summary
    print("\n📋 Your Mapping:")
    v_attrs = [a for a, p in mapping.items() if p == 'V (Value)']
    a_attrs = [a for a, p in mapping.items() if p == 'A (Access)']
    e_attrs = [a for a, p in mapping.items() if p == 'E (Evidence)']
    ex_attrs = [a for a, p in mapping.items() if p == 'Exclude']

    if v_attrs: print(f"   V (Value):    {', '.join(v_attrs)}")
    if a_attrs: print(f"   A (Access):   {', '.join(a_attrs)}")
    if e_attrs: print(f"   E (Evidence): {', '.join(e_attrs)}")
    if ex_attrs: print(f"   Excluded:     {', '.join(ex_attrs)}")

    # Mean by segment
    if 'Segment' in vae_df.columns:
        print("\n" + "="*60)
        print("MEAN V/A/E BY SEGMENT")
        print("="*60)
        seg_vae = vae_df.groupby('Segment')[['V', 'A', 'E']].mean()
        print(seg_vae.round(2))

    # Overall means
    print("\nOverall means:")
    print(vae_df[['V', 'A', 'E']].mean().round(2))

    # -------------------------------------------------------------------------
    # Scatterplot: V vs A, colored by segment
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("TRACTION LANDSCAPE: V vs. A")
    print("="*60)
    print("   Top-right = high Value + high Access (easy wins)")
    print("   Bottom-left = low everything (the 'None' choosers)")
    print("   The diagonal frontier is where trade-offs live.")

    fig, ax = plt.subplots(figsize=(9, 7))

    if 'Segment' in vae_df.columns:
        segments = sorted(vae_df['Segment'].unique())
        colors = ['#E37222', '#003366', '#64748b'][:len(segments)]
        for seg, col in zip(segments, colors):
            subset = vae_df[vae_df['Segment'] == seg]
            ax.scatter(subset['A'], subset['V'], alpha=0.5, s=40, 
                       color=col, edgecolor='white', linewidth=0.5, label=seg)
        ax.legend(title='Segment', loc='best')
    else:
        ax.scatter(vae_df['A'], vae_df['V'], alpha=0.5, s=40, 
                   color='#003366', edgecolor='white', linewidth=0.5)

    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--')
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--')
    ax.set_xlabel('A — Access (price, service, charging)', fontsize=12)
    ax.set_ylabel('V — Value (range, smart, performance)', fontsize=12)
    ax.set_title('Traction Landscape: V vs. A by Segment', fontsize=13, color='#003366')
    plt.tight_layout()
    plt.show()

    # -------------------------------------------------------------------------
    # E as color: separate plot
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("EVIDENCE (E) DISTRIBUTION")
    print("="*60)

    fig, ax = plt.subplots(figsize=(9, 5))
    if 'Segment' in vae_df.columns:
        seg_colors = {'Tech': '#E37222', 'Pragmatist': '#003366', 'PriceHunter': '#64748b'}
        for seg in sorted(vae_df['Segment'].unique()):
            subset = vae_df[vae_df['Segment'] == seg]
            ax.hist(subset['E'], bins=20, alpha=0.6, label=seg, 
                    color=seg_colors.get(seg, '#333333'), edgecolor='white')
        ax.legend(title='Segment')
    else:
        ax.hist(vae_df['E'], bins=20, alpha=0.7, color='#003366', edgecolor='white')

    ax.set_xlabel('E — Evidence (warranty, brand, trust)', fontsize=12)
    ax.set_ylabel('Number of Respondents', fontsize=12)
    ax.set_title('Distribution of Evidence Scores', fontsize=13, color='#003366')
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--')
    plt.tight_layout()
    plt.show()

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
        <h3>Pause and Reflect: Where Is the Chasm?</h3>
        <p>Look at the traction landscape. Which segment is stuck in the bottom-left? Which segment has high V but low A?</p>
        <table class="scribble-table">
          <thead>
            <tr><th>Question</th><th>My Answer</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>Which segment has the highest V but the lowest A? What does that mean?</td>
              <td><textarea placeholder="e.g., Tech has high V (smart features) but moderate A (price insensitive) — they buy despite friction..."></textarea></td>
            </tr>
            <tr>
              <td>Which segment has high A but low E? What product would fix their E?</td>
              <td><textarea placeholder="e.g., PriceHunters have high A (price sensitive) but low E (don't trust new brands) — Honda badge would help..."></textarea></td>
            </tr>
            <tr>
              <td>If Traction = V × A × E, which segment is the hardest to win?</td>
              <td><textarea placeholder="..."></textarea></td>
            </tr>
            <tr>
              <td>Did your V/A/E mapping match your prediction from the theory cell?</td>
              <td><textarea placeholder="Surprises? Confirmations?"></textarea></td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top:12px;"><strong>Next:</strong> Run the simulator with VAE overlay to see how each product configuration scores on all three pillars.</p>
      </div>
    </div>
    """
    display(HTML(html_content))

    # Reset / New Mapping buttons
    print("\n" + "-"*60)
    print("Want to try a different mapping?")
    print("-"*60)

    btn_row = widgets.HBox([
        widgets.Button(description="↺ Remap Attributes", button_style='warning', layout=widgets.Layout(width='200px', height='40px')),
        widgets.Button(description="▶ VAE Overlay on Simulator", button_style='primary', layout=widgets.Layout(width='220px', height='40px', margin='0 0 0 10px'))
    ])
    btn_row.children[0].on_click(lambda b: show_mapping_ui())
    btn_row.children[1].on_click(lambda b: show_vae_overlay_hint())
    display(btn_row)

def show_vae_overlay_hint():
    clear_output(wait=True)
    print("="*60)
    print("VAE OVERLAY")
    print("="*60)
    print("\nThe VAE overlay is available in the simulator (Step 5b).")
    print("After running a simulation, the VAE decomposition will appear")
    print("automatically if vae_df and vae_mapping are in globals.")
    print("\nTo see it now, run 05b_simulator.py and simulate a product configuration.")

if proceed:
    show_mapping_ui()
