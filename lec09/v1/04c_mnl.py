# -*- coding: utf-8 -*-
"""
Lec09 — Step 4c Code: Aggregate MNL + WTP + Segment Patterns (Generic)
Pure code cell. Run AFTER 04b_upload.py in a separate Colab cell.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/04c_mnl.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

_state = {'df': None, 'mapping': None}

# =============================================================================
# 1. Retrieve CBC data + mapping from Step 4b
# =============================================================================

if 'cbc_df' in globals() and 'cbc_mapping' in globals():
    _state['df'] = globals()['cbc_df']
    _state['mapping'] = globals()['cbc_mapping']
    print("✓ Using CBC data and mapping from Step 4b")
    proceed = True
else:
    print("⚠ CBC data not found. Please run Step 4b first, or upload below:")
    proceed = False

    upload_widget = widgets.FileUpload(accept='.csv', multiple=False, description='Upload CBC CSV')
    def on_upload(change):
        if not upload_widget.value:
            return
        file_info = list(upload_widget.value.values())[0]
        with open('/tmp/cbc.csv', 'wb') as f:
            f.write(file_info['content'])
        df = pd.read_csv('/tmp/cbc.csv')
        _state['df'] = df
        clear_output(wait=True)
        print(f"✓ Loaded {len(df)} rows")
        # Quick mapping
        cols = list(df.columns)
        dd_resp = widgets.Dropdown(options=cols, value=next((c for c in cols if 'resp' in c.lower()), cols[0]), description='Resp ID:', layout=widgets.Layout(width='350px'))
        dd_choice = widgets.Dropdown(options=cols, value=next((c for c in cols if 'chosen' in c.lower() or 'choice' in c.lower()), cols[-1]), description='Choice:', layout=widgets.Layout(width='350px'))
        attr_sel = widgets.SelectMultiple(options=cols, description='Attributes:', layout=widgets.Layout(width='350px', height='150px'))
        def upd(*args):
            attr_sel.options = [c for c in cols if c not in {dd_resp.value, dd_choice.value}]
        dd_resp.observe(upd, names='value')
        dd_choice.observe(upd, names='value')
        upd()
        btn = widgets.Button(description='✓ Confirm', button_style='success')
        def on_conf(b):
            _state['mapping'] = {'resp_id': dd_resp.value, 'choice': dd_choice.value, 'attr_cols': list(attr_sel.value), 'task_id': None, 'alt_id': None}
            show_run_button()
        btn.on_click(on_conf)
        display(widgets.VBox([dd_resp, dd_choice, attr_sel, btn]))
    upload_widget.observe(on_upload, names='value')
    display(upload_widget)

# =============================================================================
# 2. Expectation + Run button
# =============================================================================

def show_run_button():
    print("\n📋 What will happen when you click 'Run MNL Analysis':")
    print("   • Estimate aggregate multinomial logit from ~19,000 choice observations")
    print("   • Compute coefficients for each attribute level")
    print("   • Derive willingness-to-pay (WTP) from price/attribute ratios")
    print("   • Show segment-specific choice patterns and 'None' rates")
    print("   • Estimated runtime: ~5 seconds")
    print()

    run_btn = widgets.Button(
        description="▶ Run MNL Analysis",
        button_style='primary',
        layout=widgets.Layout(width='200px', height='40px')
    )
    run_btn.on_click(lambda b: run_mnl())
    display(run_btn)

# =============================================================================
# 3. Main MNL analysis
# =============================================================================

def run_mnl():
    df = _state['df']
    m = _state['mapping']
    resp_col = m['resp_id']
    choice_col = m['choice']
    attr_cols = m['attr_cols']
    task_col = m.get('task_id')
    alt_col = m.get('alt_id')

    clear_output(wait=True)
    print("="*60)
    print("AGGREGATE MULTINOMIAL LOGIT ANALYSIS")
    print("="*60)

    # -------------------------------------------------------------------------
    # 3a. Prepare dummies
    # -------------------------------------------------------------------------

    model_data = df.copy()
    dummy_cols = []

    for col in attr_cols:
        levels = sorted(model_data[col].dropna().unique())
        # Detect None/outside good
        none_vals = [v for v in levels if str(v).lower() in ['none', 'nan', '']]
        ref_level = none_vals[0] if none_vals else levels[-1]

        for lev in levels:
            if lev != ref_level:
                dname = f'd_{col}_{lev}'
                is_none = model_data[col].astype(str).str.lower().isin(['none', 'nan', ''])
                model_data[dname] = ((model_data[col] == lev) & (~is_none)).astype(int)
                dummy_cols.append(dname)

    print(f"✓ Created {len(dummy_cols)} dummy variables from {len(attr_cols)} attributes")

    # -------------------------------------------------------------------------
    # 3b. Aggregate Logistic Regression
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("AGGREGATE MNL COEFFICIENTS")
    print("="*60)
    print("   Method: Logistic regression on all alternative rows")
    print("   Positive coefficient = increases choice probability")
    print("   Negative coefficient = decreases choice probability")

    X = model_data[dummy_cols].values
    y = model_data[choice_col].values

    logit = LogisticRegression(max_iter=1000, class_weight='balanced', solver='lbfgs')
    logit.fit(X, y)

    coef_df = pd.DataFrame({
        'Attribute_Level': dummy_cols,
        'Coefficient': logit.coef_[0]
    }).sort_values('Coefficient', ascending=False)

    print("\n")
    print(coef_df.round(3).to_string(index=False))

    # Bar chart
    fig, ax = plt.subplots(figsize=(10, 5.5))
    coef_sorted = coef_df.sort_values('Coefficient', ascending=True)
    colors = ['#E37222' if v == coef_sorted['Coefficient'].max() else '#003366' for v in coef_sorted['Coefficient']]
    ax.barh(coef_sorted['Attribute_Level'], coef_sorted['Coefficient'], color=colors, edgecolor='white')
    ax.set_xlabel('Logit Coefficient', fontsize=12)
    ax.set_title('What Drives Choice? (higher = more likely chosen)', fontsize=13, color='#003366')
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
    for i, v in enumerate(coef_sorted['Coefficient']):
        ax.text(v + 0.02 if v >= 0 else v - 0.02, i, f'{v:.2f}', 
                va='center', ha='left' if v >= 0 else 'right', fontsize=9)
    plt.tight_layout()
    plt.show()

    # -------------------------------------------------------------------------
    # 3c. Explicit WTP with formula
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("WILLINGNESS-TO-PAY (WTP)")
    print("="*60)
    print("   Formula: WTP(attribute) = −β_attribute / β_price")
    print("   This tells you how much rupees one attribute level is worth.")

    price_coefs = coef_df[coef_df['Attribute_Level'].str.contains('_Price_')]
    if len(price_coefs) > 0:
        price_num = price_coefs.loc[price_coefs['Coefficient'].idxmin()]
        beta_price = price_num['Coefficient']
        print(f"\n   Price numeraire: {price_num['Attribute_Level']} = {beta_price:.3f}")
        print(f"   (This is the most negative price coefficient — the baseline price effect)")
        print("\n   WTP calculations:")

        wtp_rows = []
        for _, row in coef_df.iterrows():
            if 'Price' not in row['Attribute_Level'] and beta_price != 0:
                wtp = -row['Coefficient'] / beta_price
                wtp_rows.append({
                    'Attribute': row['Attribute_Level'],
                    'Beta': row['Coefficient'],
                    'WTP': wtp
                })

        wtp_df = pd.DataFrame(wtp_rows).sort_values('WTP', ascending=False)
        print(wtp_df.round(3).to_string(index=False))

        # WTP bar chart
        fig, ax = plt.subplots(figsize=(9, 4.5))
        wtp_sorted = wtp_df.sort_values('WTP', ascending=True)
        colors = ['#E37222' if v > 0 else '#64748b' for v in wtp_sorted['WTP']]
        ax.barh(wtp_sorted['Attribute'], wtp_sorted['WTP'], color=colors, edgecolor='white')
        ax.set_xlabel('WTP (in price units)', fontsize=12)
        ax.set_title('Willingness-to-Pay by Attribute Level', fontsize=13, color='#003366')
        ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
        for i, v in enumerate(wtp_sorted['WTP']):
            ax.text(v + 0.02 if v >= 0 else v - 0.02, i, f'{v:.2f}', 
                    va='center', ha='left' if v >= 0 else 'right', fontsize=9)
        plt.tight_layout()
        plt.show()
    else:
        print("   (No price dummy found — WTP cannot be computed)")

    # -------------------------------------------------------------------------
    # 3d. Segment-specific choice patterns
    # -------------------------------------------------------------------------

    if 'Segment' in df.columns:
        print("\n" + "="*60)
        print("SEGMENT-SPECIFIC CHOICE PATTERNS")
        print("="*60)

        chosen_data = model_data[model_data[choice_col] == 1]

        for seg in sorted(df['Segment'].unique()):
            seg_chosen = chosen_data[chosen_data['Segment'] == seg]
            if len(seg_chosen) == 0:
                continue
            print(f"\n{seg} (n={len(seg_chosen)} choices):")

            shares = {}
            for dc in dummy_cols[:6]:
                shares[dc.replace('d_', '')] = seg_chosen[dc].mean()

            # None rate
            if alt_col:
                max_alt = df[alt_col].max()
                none_rate = (seg_chosen[alt_col] == max_alt).mean()
            else:
                none_rate = seg_chosen[attr_cols[0]].astype(str).str.lower().isin(['none', 'nan']).mean()
            shares['None (outside good)'] = none_rate

            for attr, share in sorted(shares.items(), key=lambda x: -x[1]):
                print(f"  {attr:25s}: {share:.3f}")

    # -------------------------------------------------------------------------
    # 3e. None rate by segment
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("'NONE OF THESE' CHOICE RATE")
    print("="*60)

    chosen_data = model_data[model_data[choice_col] == 1]

    if 'Segment' in df.columns and alt_col:
        none_rates = {}
        for seg in sorted(df['Segment'].unique()):
            seg_chosen = chosen_data[chosen_data['Segment'] == seg]
            max_alt = df[alt_col].max()
            none_rate = (seg_chosen[alt_col] == max_alt).mean()
            none_rates[seg] = none_rate

        none_series = pd.Series(none_rates).sort_values(ascending=False)
        print(none_series.round(3))

        fig, ax = plt.subplots(figsize=(7, 4))
        bar_colors = ['#E37222', '#003366', '#64748b'][:len(none_series)]
        bars = ax.bar(none_series.index, none_series.values * 100, color=bar_colors, edgecolor='white')
        ax.set_ylabel('None Choice Rate (%)', fontsize=12)
        ax.set_title('"None of These" by Segment', fontsize=13, color='#003366')
        for bar, val in zip(bars, none_series.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{val*100:.1f}%', ha='center', fontsize=11)
        plt.tight_layout()
        plt.show()
    else:
        if alt_col:
            max_alt = df[alt_col].max()
            overall_none = (chosen_data[alt_col] == max_alt).mean()
        else:
            overall_none = chosen_data[attr_cols[0]].astype(str).str.lower().isin(['none', 'nan']).mean()
        print(f"Overall None rate: {overall_none:.1%}")

    # -------------------------------------------------------------------------
    # 3f. Scribble pause: Metric vs CBC
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
        <h3>Pause and Reflect: Metric vs. CBC — Do They Agree?</h3>
        <p>The metric conjoint asked "How much do you like this?" The CBC asked "Which one would you actually buy?" These are different questions. Do they give the same answer?</p>
        <table class="scribble-table">
          <thead>
            <tr><th>Question</th><th>Metric Conjoint Said</th><th>CBC Says</th><th>Verdict</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>Most important attribute</td>
              <td><textarea placeholder="From Step 3 importance chart..."></textarea></td>
              <td><textarea placeholder="From MNL coefficients above..."></textarea></td>
              <td><textarea placeholder="Agree / Disagree / Partially..."></textarea></td>
            </tr>
            <tr>
              <td>Which segment chooses "None" most?</td>
              <td><textarea placeholder="Who had lowest ratings?"></textarea></td>
              <td><textarea placeholder="Check None rate chart above..."></textarea></td>
              <td><textarea placeholder="..."></textarea></td>
            </tr>
            <tr>
              <td>Why might metric and CBC diverge for PriceHunters?</td>
              <td colspan="3"><textarea placeholder="e.g., Ratings = desire; Choice = constrained by budget and competition. PriceHunters may rate a cheap product highly but still choose None if even the cheapest option is too expensive..."></textarea></td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top:12px;"><strong>Key insight:</strong> Where the two methods disagree, trust the CBC. Ratings measure <em>desire</em>; choices measure <em>decisions</em> under budget and competitive pressure. The gap between desire and decision is where your pricing and positioning strategy lives.</p>
        <p><strong>Next:</strong> Run 05_simulator.py to project market share for candidate product configurations against real competitors.</p>
      </div>
    </div>
    """))

if proceed:
    show_run_button()
