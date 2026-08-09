# -*- coding: utf-8 -*-
"""
Lec09 — Step 5b: Market Simulator (Generic)
Auto-detects reference levels. Features: pie chart, reset button, no re-upload.
Pure code cell. Run AFTER 05a_theory.py in a separate Colab cell.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/05b_simulator.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

_state = {'ib_df': None, 'orig_df': None, 'attr_map': None, 'ref_names': None,
          'product_widgets': None, 'none_util': None}

# =============================================================================
# 1. Entry point: check if data already loaded
# =============================================================================

def entry_point():
    if _state['ib_df'] is not None and _state['ref_names'] is not None:
        # Data already loaded from a previous run — go straight to configurator
        show_configurator()
    elif 'ib_df' in globals():
        _state['ib_df'] = globals()['ib_df']
        print("✓ Using ib_df from Step 3")
        ask_for_original()
    else:
        print("⚠ ib_df not found. Please upload your individual part-worths CSV below:")
        upload_ib = widgets.FileUpload(accept='.csv', multiple=False, description='Upload Part-Worths CSV')
        def on_upload_ib(change):
            if not upload_ib.value:
                return
            file_info = list(upload_ib.value.values())[0]
            with open('/tmp/ib.csv', 'wb') as f:
                f.write(file_info['content'])
            ib_df = pd.read_csv('/tmp/ib.csv')
            _state['ib_df'] = ib_df
            globals()['ib_df'] = ib_df
            clear_output(wait=True)
            print(f"✓ Loaded {len(ib_df)} respondent part-worth profiles")
            ask_for_original()
        upload_ib.observe(on_upload_ib, names='value')
        display(upload_ib)

# =============================================================================
# 2. Retrieve or upload original data
# =============================================================================

def ask_for_original():
    clear_output(wait=True)
    print("="*60)
    print("STEP 1: PROVIDE ORIGINAL DATA FOR REFERENCE LEVEL DETECTION")
    print("="*60)
    print("\nTo auto-detect reference (baseline) levels, I need the original")
    print("conjoint data (metric or CBC) that contains ALL attribute levels.")
    print()

    orig_options = []
    for key in ['metric_df', 'cbc_df']:
        if key in globals():
            orig_options.append(key)

    if orig_options:
        print("✓ Found original data in workspace:")
        for opt in orig_options:
            print(f"   • {opt} ({len(globals()[opt])} rows)")
        print("\nSelect which one to use, or upload a fresh CSV:")
    else:
        print("No original data found in workspace. Please upload below:")

    choices = ['(Upload new CSV)'] + orig_options
    dd_orig = widgets.Dropdown(options=choices, value=choices[0], description='Source:', layout=widgets.Layout(width='350px'))
    upload_orig = widgets.FileUpload(accept='.csv', multiple=False, description='Upload Original CSV', layout=widgets.Layout(width='200px'))

    def on_select(change):
        if dd_orig.value != '(Upload new CSV)':
            _state['orig_df'] = globals()[dd_orig.value]
            clear_output(wait=True)
            print(f"✓ Using {dd_orig.value} from workspace")
            detect_references()

    dd_orig.observe(on_select, names='value')

    def on_upload_orig(change):
        if not upload_orig.value:
            return
        file_info = list(upload_orig.value.values())[0]
        with open('/tmp/orig.csv', 'wb') as f:
            f.write(file_info['content'])
        orig_df = pd.read_csv('/tmp/orig.csv')
        _state['orig_df'] = orig_df
        clear_output(wait=True)
        print(f"✓ Loaded original data: {len(orig_df)} rows")
        detect_references()

    upload_orig.observe(on_upload_orig, names='value')
    display(widgets.VBox([dd_orig, upload_orig]))

# =============================================================================
# 3. Auto-detect reference levels
# =============================================================================

def detect_references():
    ib_df = _state['ib_df']
    orig_df = _state['orig_df']

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
        attr_map.setdefault(attr, {'dummy_levels': set()})
        attr_map[attr]['dummy_levels'].add(level)

    ref_names = {}
    missing_attrs = []

    for attr in attr_map:
        if attr in orig_df.columns:
            all_levels = set(orig_df[attr].dropna().unique().astype(str))
            dummy_levels = attr_map[attr]['dummy_levels']
            ref_candidates = all_levels - dummy_levels
            ref_candidates = {r for r in ref_candidates if r.lower() not in ['none', 'nan', '']}

            if len(ref_candidates) == 1:
                ref_names[attr] = list(ref_candidates)[0]
            elif len(ref_candidates) > 1:
                freq = orig_df[orig_df[attr].astype(str).isin(ref_candidates)][attr].value_counts()
                ref_names[attr] = freq.index[0]
            else:
                missing_attrs.append(attr)
        else:
            missing_attrs.append(attr)

    if missing_attrs:
        print(f"\n⚠ Could not auto-detect reference for: {', '.join(missing_attrs)}")
        print("Please specify manually:")
        manual_inputs = {}
        for attr in missing_attrs:
            txt = widgets.Text(value='', placeholder=f'Reference level for {attr}', description=f'{attr}:', layout=widgets.Layout(width='300px'))
            manual_inputs[attr] = txt
            display(txt)

        def on_manual(b):
            for attr in missing_attrs:
                ref_names[attr] = manual_inputs[attr].value.strip() or f"{attr}_ref"
            _state['ref_names'] = ref_names
            _state['attr_map'] = attr_map
            show_configurator()

        btn = widgets.Button(description="✓ Confirm", button_style='success')
        btn.on_click(on_manual)
        display(btn)
    else:
        _state['ref_names'] = ref_names
        _state['attr_map'] = attr_map
        show_configurator()

# =============================================================================
# 4. Build product configurator
# =============================================================================

def show_configurator():
    attr_map = _state['attr_map']
    ref_names = _state['ref_names']
    attrs = list(attr_map.keys())

    clear_output(wait=True)
    print("="*60)
    print("MARKET SIMULATOR: CONFIGURE YOUR PRODUCTS")
    print("="*60)

    # Reference levels table
    print("\n📋 AUTO-DETECTED REFERENCE LEVELS (Baseline = 0 utility)")
    print("   These levels were omitted in the regression. All part-worths are relative to them.")
    print()

    ref_data = []
    for attr in attrs:
        non_ref = sorted(attr_map[attr]['dummy_levels'])
        ref_data.append({
            'Attribute': attr,
            'Reference Level (utility = 0)': ref_names[attr],
            'Non-Reference Levels (have part-worths)': ', '.join(non_ref)
        })
    ref_df = pd.DataFrame(ref_data)
    display(ref_df)

    print("\n" + "-"*60)
    print("Set the attribute levels for each product in the competitive set.")
    print("Select the reference level name to set utility = 0 for that attribute.")
    print()

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
            levels = sorted(attr_map[attr]['dummy_levels']) + [ref_names[attr]]
            dd = widgets.Dropdown(
                options=levels,
                value=ref_names[attr],
                description=f'{attr}:',
                layout=widgets.Layout(width='250px'),
                style={'description_width': '70px'}
            )
            attr_dropdowns[attr] = dd
            row_widgets.append(dd)

        for i in range(0, len(row_widgets), 4):
            display(widgets.HBox(row_widgets[i:i+4]))

        product_widgets[prod_key] = attr_dropdowns

    none_util = widgets.FloatSlider(
        value=0.0, min=-3.0, max=1.0, step=0.1,
        description='None utility:', layout=widgets.Layout(width='400px'),
        style={'description_width': '100px'}
    )
    print("\n'None of these' option utility (0 = neutral, negative = less attractive):")
    display(none_util)

    _state['product_widgets'] = product_widgets
    _state['none_util'] = none_util

    print("\n" + "-"*60)
    print("📋 What will happen when you click 'Simulate Market':")
    print("   • Compute utility for each product using every respondent's part-worths")
    print("   • Apply logit choice rule: P = exp(U) / sum(exp(all U))")
    print("   • Average across all respondents → market share projection")
    print("   • Show overall share as PIE CHART + segment-specific shares")
    print("   • Estimated runtime: ~3 seconds")
    print()

    btn_row = widgets.HBox([
        widgets.Button(
            description="▶ Simulate Market",
            button_style='primary',
            layout=widgets.Layout(width='200px', height='40px')
        ),
        widgets.Button(
            description="↺ Reset to Defaults",
            button_style='warning',
            layout=widgets.Layout(width='180px', height='40px', margin='0 0 0 10px')
        )
    ])

    btn_row.children[0].on_click(lambda b: run_simulation())
    btn_row.children[1].on_click(lambda b: reset_configurator())
    display(btn_row)

# =============================================================================
# 5. Reset configurator (no re-upload)
# =============================================================================

def reset_configurator():
    """Reset all dropdowns to reference levels without re-uploading data."""
    show_configurator()

# =============================================================================
# 6. Run simulation
# =============================================================================

def run_simulation():
    ib_df = _state['ib_df']
    attr_map = _state['attr_map']
    ref_names = _state['ref_names']
    product_widgets = _state['product_widgets']
    none_util = _state['none_util'].value

    clear_output(wait=True)
    print("="*60)
    print("MARKET SIMULATION RESULTS")
    print("="*60)

    products = []
    for prod_key in ['Yana', 'Comp A', 'Comp B']:
        config = {}
        for attr, dd in product_widgets[prod_key].items():
            config[attr] = dd.value
        products.append({'name': prod_key, 'config': config})

    print("\n📦 Configured Products:")
    for p in products:
        cfg_str = ', '.join([f"{k}={v}" for k, v in p['config'].items()])
        print(f"   {p['name']}: {cfg_str}")
    print(f"   None of these: utility = {none_util:.1f}")

    pw_cols = [c for c in ib_df.columns if c not in ['RespID', 'Segment', 'Intercept', 'Cluster']]

    results = []
    for _, resp in ib_df.iterrows():
        utilities = []
        for prod in products:
            u = 0.0
            for attr, level in prod['config'].items():
                if level == ref_names[attr]:
                    u += 0.0
                else:
                    dummy_col = f'd_{attr}_{level}'
                    if dummy_col in resp:
                        u += float(resp[dummy_col]) if pd.notna(resp[dummy_col]) else 0.0
            utilities.append(u)

        utilities.append(none_util)

        max_u = max(utilities)
        exp_u = np.exp(np.array(utilities) - max_u)
        probs = exp_u / exp_u.sum()

        row = {'RespID': resp['RespID']}
        if 'Segment' in resp:
            row['Segment'] = resp['Segment']
        for i, prod in enumerate(products):
            row[f'P_{prod["name"]}'] = probs[i]
        row['P_None'] = probs[-1]
        results.append(row)

    sim_df = pd.DataFrame(results)

    # Overall shares — PIE CHART
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

    fig, ax = plt.subplots(figsize=(8, 8))
    labels = share_table['Product'].tolist()
    sizes = share_table['Share (%)'].tolist()
    colors = ['#E37222', '#003366', '#22c55e', '#64748b']
    explode = [0.05 if 'Yana' in label else 0 for label in labels]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        autopct='%1.1f%%', startangle=90, pctdistance=0.75,
        wedgeprops=dict(edgecolor='white', linewidth=2)
    )
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    for text in texts:
        text.set_fontsize(11)

    ax.set_title('Predicted Market Share', fontsize=14, color='#003366', pad=20)
    plt.tight_layout()
    plt.show()

    # Segment-specific shares
    if 'Segment' in sim_df.columns:
        print("\n" + "="*60)
        print("SEGMENT-SPECIFIC SHARES")
        print("="*60)

        seg_shares = sim_df.groupby('Segment')[share_cols].mean() * 100
        print(seg_shares.round(1))

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

    globals()['sim_df'] = sim_df

    # Scribble pause
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
      </div>
    </div>
    """
    display(HTML(html_content))

    # Reset / New Simulation buttons
    print("\n" + "-"*60)
    print("What next?")
    print("-"*60)

    btn_row = widgets.HBox([
        widgets.Button(
            description="↺ Reset Configurations",
            button_style='warning',
            layout=widgets.Layout(width='200px', height='40px')
        ),
        widgets.Button(
            description="▶ New Simulation",
            button_style='primary',
            layout=widgets.Layout(width='200px', height='40px', margin='0 0 0 10px')
        )
    ])
    btn_row.children[0].on_click(lambda b: reset_configurator())
    btn_row.children[1].on_click(lambda b: show_configurator())
    display(btn_row)

# =============================================================================
# 7. Start
# =============================================================================

entry_point()
