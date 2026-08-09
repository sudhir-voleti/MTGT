# -*- coding: utf-8 -*-
"""
Lec09 — Step 3: Individual-Level OLS Part-Worth Estimation (Generic)
Interactive: sample respondent walkthrough, then 'Run Analysis' button.
No clustering — that lives in 03b_segmentation.py.
Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/03_individual_ols.py').text)
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

_state = {'df': None, 'mapping': None, 'ib_df': None}

# =============================================================================
# 1. Retrieve data + mapping from Step 2, or prompt for upload
# =============================================================================

if 'metric_df' in globals() and 'col_mapping' in globals():
    _state['df'] = globals()['metric_df']
    _state['mapping'] = globals()['col_mapping']
    print("✓ Using data and column mapping from Step 2")
    proceed = True
else:
    print("⚠ Step 2 data not found. Please upload your metric conjoint CSV below:")
    proceed = False

    upload_widget = widgets.FileUpload(accept='.csv', multiple=False, description='Upload CSV')
    def on_upload(change):
        if not upload_widget.value:
            return
        file_info = list(upload_widget.value.values())[0]
        with open('/tmp/metric.csv', 'wb') as f:
            f.write(file_info['content'])
        df = pd.read_csv('/tmp/metric.csv')
        _state['df'] = df
        clear_output(wait=True)
        print("📋 Columns:", list(df.columns))
        cols = list(df.columns)
        numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
        dd_resp = widgets.Dropdown(options=cols, value=next((c for c in cols if 'resp' in c.lower()), cols[0]), description='Resp ID:', layout=widgets.Layout(width='350px'))
        dd_y = widgets.Dropdown(options=cols, value=next((c for c in numeric_cols if 'rating' in c.lower()), numeric_cols[0] if numeric_cols else cols[0]), description='Rating Y:', layout=widgets.Layout(width='350px'))
        attr_sel = widgets.SelectMultiple(options=cols, description='Attributes:', layout=widgets.Layout(width='350px', height='150px'))
        def upd(*args):
            rsv = {dd_resp.value, dd_y.value}
            attr_sel.options = [c for c in cols if c not in rsv]
        dd_resp.observe(upd, names='value')
        dd_y.observe(upd, names='value')
        upd()
        btn = widgets.Button(description='✓ Confirm', button_style='success')
        def on_conf(b):
            _state['mapping'] = {'resp_id': dd_resp.value, 'y_col': dd_y.value, 'attr_cols': list(attr_sel.value)}
            show_sample_then_button()
        btn.on_click(on_conf)
        display(widgets.VBox([dd_resp, dd_y, attr_sel, btn]))
    upload_widget.observe(on_upload, names='value')
    display(upload_widget)

# =============================================================================
# 2. Sample respondent walkthrough (always shown first)
# =============================================================================

def show_sample_then_button():
    df = _state['df']
    m = _state['mapping']
    resp_col = m['resp_id']
    y_col = m['y_col']
    attr_cols = m['attr_cols']

    clear_output(wait=True)
    print("="*60)
    print("SAMPLE RESPONDENT: What One Regression Looks Like")
    print("="*60)

    sample_resp = df[resp_col].iloc[0]
    sample_data = df[df[resp_col] == sample_resp].copy()

    print(f"\nRespondent {sample_resp} rated {len(sample_data)} profiles.")
    print("We run one OLS regression on their ratings, with attribute dummies as predictors.")

    # Build dummies for sample
    dummy_cols = []
    for col in attr_cols:
        levels = sorted(sample_data[col].dropna().unique())
        ref = levels[-1]
        for lev in levels[:-1]:
            dname = f'd_{col}_{lev}'
            sample_data[dname] = (sample_data[col] == lev).astype(int)
            dummy_cols.append(dname)

    if dummy_cols:
        Xs = sample_data[dummy_cols]
        Xs = sm.add_constant(Xs)
        ys = sample_data[y_col]
        try:
            ms = sm.OLS(ys, Xs).fit()
            print(f"\n   R-squared: {ms.rsquared:.3f}")
            print(f"   Coefficients (part-worths relative to reference levels):")
            for param, val in ms.params.items():
                if param != 'const':
                    print(f"      {param:25s}: {val:7.3f}")
        except Exception as e:
            print(f"   (Sample regression failed: {e})")

    print("\n" + "-"*60)
    print("Now imagine running this same regression for EVERY respondent.")
    print("That gives us one part-worth profile per person — 400 in total.")
    print("-"*60)

    # Expectation + Run button
    print("\n📋 What will happen when you click 'Run Analysis':")
    print("   • Estimate 400 individual OLS models (one per respondent)")
    print("   • Compute attribute importance for each person")
    print("   • Show overall importance bar chart")
    print("   • Display 3 sample individual part-worth profiles as mini charts")
    print("   • Estimated runtime: ~10 seconds")
    print()

    run_btn = widgets.Button(
        description="▶ Run Analysis",
        button_style='primary',
        layout=widgets.Layout(width='180px', height='40px')
    )
    run_btn.on_click(lambda b: run_analysis())
    display(run_btn)

# =============================================================================
# 3. Main analysis (triggered by button)
# =============================================================================

def run_analysis():
    df = _state['df']
    m = _state['mapping']
    resp_col = m['resp_id']
    y_col = m['y_col']
    attr_cols = m['attr_cols']

    clear_output(wait=True)
    print("="*60)
    print("RUNNING INDIVIDUAL-LEVEL OLS ANALYSIS")
    print("="*60)

    individual_betas = []
    n_converged = 0

    for resp_id in df[resp_col].unique():
        resp_data = df[df[resp_col] == resp_id].copy()

        dummy_cols = []
        for col in attr_cols:
            levels = sorted(resp_data[col].dropna().unique())
            ref = levels[-1]
            for lev in levels[:-1]:
                dname = f'd_{col}_{lev}'
                resp_data[dname] = (resp_data[col] == lev).astype(int)
                dummy_cols.append(dname)

        if len(dummy_cols) == 0:
            continue

        Xi = resp_data[dummy_cols]
        Xi = sm.add_constant(Xi)
        yi = resp_data[y_col]

        try:
            mi = sm.OLS(yi, Xi).fit()
            row = {'RespID': resp_id}
            if 'Segment' in resp_data.columns:
                row['Segment'] = resp_data['Segment'].iloc[0]
            row['Intercept'] = mi.params.get('const', np.nan)
            for dc in dummy_cols:
                row[dc] = mi.params.get(dc, np.nan)
            individual_betas.append(row)
            n_converged += 1
        except:
            pass

    ib_df = pd.DataFrame(individual_betas)
    _state['ib_df'] = ib_df
    globals()['ib_df'] = ib_df

    print(f"✓ Individual models estimated: {n_converged} / {df[resp_col].nunique()}")

    # -------------------------------------------------------------------------
    # Attribute Importance
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("ATTRIBUTE IMPORTANCE")
    print("="*60)

    pw_cols = [c for c in ib_df.columns if c not in ['RespID', 'Segment', 'Intercept']]

    attr_groups = {}
    for c in pw_cols:
        parts = c.split('_', 2)
        if len(parts) >= 2:
            attr_groups.setdefault(parts[1], []).append(c)

    def compute_imp(row):
        imps = {}
        for attr, dcols in attr_groups.items():
            pws = [0] + [float(row.get(dc, 0)) for dc in dcols if pd.notna(row.get(dc, np.nan))]
            pws = [v for v in pws if not pd.isna(v)]
            imps[attr] = max(pws) - min(pws) if pws else 0
        total = sum(imps.values())
        if total == 0:
            return pd.Series([np.nan]*len(attr_groups), index=list(attr_groups.keys()))
        return pd.Series({k: v/total*100 for k, v in imps.items()})

    importance = ib_df.apply(compute_imp, axis=1)
    importance['RespID'] = ib_df['RespID']
    if 'Segment' in ib_df.columns:
        importance['Segment'] = ib_df['Segment']

    imp_overall = importance[[c for c in importance.columns if c not in ['RespID', 'Segment']]].mean()
    print("\nOverall attribute importance (%):")
    print(imp_overall.round(1).sort_values(ascending=False))

    if 'Segment' in importance.columns:
        imp_by_seg = importance.groupby('Segment')[[c for c in importance.columns if c not in ['RespID', 'Segment']]].mean()
        print("\nBy segment:")
        print(imp_by_seg.round(1))

    fig, ax = plt.subplots(figsize=(9, 4.5))
    imp_sorted = imp_overall.sort_values(ascending=True)
    colors = ['#E37222' if v == imp_sorted.max() else '#003366' for v in imp_sorted]
    ax.barh(imp_sorted.index, imp_sorted.values, color=colors, edgecolor='white')
    ax.set_xlabel('Importance (%)', fontsize=12)
    ax.set_title('Overall Attribute Importance', fontsize=13, color='#003366')
    for i, v in enumerate(imp_sorted.values):
        ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=10)
    plt.tight_layout()
    plt.show()

    globals()['importance'] = importance

    # -------------------------------------------------------------------------
    # 3 sample sparkline profiles
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("SAMPLE INDIVIDUAL PART-WORTH PROFILES")
    print("="*60)
    print("Each bar chart shows one respondent's estimated part-worths.")
    print("Notice the heterogeneity — these are 3 random people from the same 400.")

    sample_ids = ib_df['RespID'].head(3).values
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.5))
    for idx, sid in enumerate(sample_ids):
        row = ib_df[ib_df['RespID'] == sid].iloc[0]
        seg = row.get('Segment', 'Unknown')
        coeffs = {k: v for k, v in row.items() if k not in ['RespID', 'Segment', 'Intercept'] and pd.notna(v)}
        names = list(coeffs.keys())
        vals = list(coeffs.values())
        colors = ['#E37222' if v > 0 else '#64748b' for v in vals]
        axes[idx].barh(names, vals, color=colors, edgecolor='white')
        axes[idx].set_title(f'Resp {sid} ({seg})', fontsize=11, color='#003366')
        axes[idx].axvline(x=0, color='gray', linewidth=0.8)
        axes[idx].set_xlabel('Part-worth', fontsize=9)
    plt.tight_layout()
    plt.show()

    # -------------------------------------------------------------------------
    # Store + next-step prompt
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("✓ Part-worths estimated for all respondents")
    print("✓ Attribute importance computed")
    print("✓ Sample profiles displayed")
    print("\nNext: Run 03b_segmentation.py to discover respondent clusters.")
    print("      Or run 03c_explore.py to build custom scatterplots.")

if proceed:
    show_sample_then_button()
