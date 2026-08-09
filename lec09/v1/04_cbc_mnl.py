# -*- coding: utf-8 -*-
"""
Lec09 — Step 4: CBC Analysis (Aggregate MNL + WTP)
Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/04_cbc_mnl.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display
import ipywidgets as widgets

# =============================================================================
# 1. Retrieve or re-upload CBC data
# =============================================================================

if 'cbc_df' in globals():
    cbc_df = globals()['cbc_df']
    print("✓ Using cbc_df from previous cell")
else:
    print("⚠ cbc_df not found. Please upload yana_cbc_n400.csv below:")
    upload_widget = widgets.FileUpload(accept='.csv', multiple=False, description='Upload CBC CSV')
    def _load(change):
        if len(upload_widget.value) > 0:
            content = upload_widget.value[0]['content']
            with open('/tmp/cbc.csv', 'wb') as f:
                f.write(content)
            globals()['cbc_df'] = pd.read_csv('/tmp/cbc.csv')
            print("✓ Loaded CBC data")
    upload_widget.observe(_load, names='value')
    display(upload_widget)
    raise SystemExit("Re-run this cell after uploading")

# =============================================================================
# 2. Prepare MNL Dummies
# =============================================================================

print("\n" + "="*60)
print("CBC DATA PREPARATION")
print("="*60)

model_data = cbc_df.copy()

model_data['d_Range_110'] = (model_data['Range'] == '110km').astype(int) * (model_data['AltID'] != 4)
model_data['d_Range_150'] = (model_data['Range'] == '150km').astype(int) * (model_data['AltID'] != 4)
model_data['d_Charge_fast'] = (model_data['Charge'] == '1.5hrs').astype(int) * (model_data['AltID'] != 4)
model_data['d_Price_85'] = (model_data['Price'] == '85K').astype(int) * (model_data['AltID'] != 4)
model_data['d_Price_110'] = (model_data['Price'] == '110K').astype(int) * (model_data['AltID'] != 4)
model_data['d_Service_100'] = (model_data['Service'] == '100cities').astype(int) * (model_data['AltID'] != 4)
model_data['d_Service_300'] = (model_data['Service'] == '300cities').astype(int) * (model_data['AltID'] != 4)
model_data['d_Smart_Adv'] = (model_data['Smart'] == 'Advanced').astype(int) * (model_data['AltID'] != 4)
model_data['d_Warr_4'] = (model_data['Warranty'] == '4yr').astype(int) * (model_data['AltID'] != 4)
model_data['d_Warr_6'] = (model_data['Warranty'] == '6yr').astype(int) * (model_data['AltID'] != 4)
model_data['d_Brand_Honda'] = (model_data['Brand'] == 'Honda').astype(int) * (model_data['AltID'] != 4)
model_data['d_Brand_Ola'] = (model_data['Brand'] == 'Ola').astype(int) * (model_data['AltID'] != 4)
model_data['d_Brand_Ather'] = (model_data['Brand'] == 'Ather').astype(int) * (model_data['AltID'] != 4)
model_data['d_None'] = (model_data['AltID'] == 4).astype(int)

chosen_data = model_data[model_data['Chosen'] == 1]

print(f"✓ Prepared {len(model_data)} rows, {len(chosen_data)} chosen observations")

# =============================================================================
# 3. Aggregate MNL Approximation (Logistic Regression)
# =============================================================================

print("\n" + "="*60)
print("AGGREGATE MNL (Logistic Regression Approximation)")
print("="*60)

# For a proper conditional logit we'd use mlogit/biogeme.
# Here we use a simplified approach: logistic regression on all rows
# with choice as binary outcome. This is pedagogically adequate.

from sklearn.linear_model import LogisticRegression

X_cols = ['d_Range_110', 'd_Range_150', 'd_Charge_fast',
          'd_Price_85', 'd_Price_110',
          'd_Service_100', 'd_Service_300',
          'd_Smart_Adv', 'd_Warr_4', 'd_Warr_6',
          'd_Brand_Honda', 'd_Brand_Ola', 'd_Brand_Ather', 'd_None']

X = model_data[X_cols].values
y = model_data['Chosen'].values

# Use class_weight to handle imbalance (None is ~15%)
logit = LogisticRegression(max_iter=1000, class_weight='balanced', solver='lbfgs')
logit.fit(X, y)

coef_df = pd.DataFrame({
    'Attribute': X_cols,
    'Coefficient': logit.coef_[0]
}).sort_values('Coefficient', ascending=False)

print("\nEstimated coefficients (higher = more likely to be chosen):")
print(coef_df.round(3).to_string(index=False))

# Bar chart
fig, ax = plt.subplots(figsize=(10, 5))
coef_sorted = coef_df.sort_values('Coefficient', ascending=True)
colors = ['#E37222' if c == coef_sorted['Coefficient'].max() else '#003366' for c in coef_sorted['Coefficient']]
ax.barh(coef_sorted['Attribute'], coef_sorted['Coefficient'], color=colors, edgecolor='white')
ax.set_xlabel('Logit Coefficient', fontsize=12)
ax.set_title('Aggregate MNL Coefficients', fontsize=13, color='#003366')
ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
for i, v in enumerate(coef_sorted['Coefficient']):
    ax.text(v + 0.02 if v >= 0 else v - 0.02, i, f'{v:.2f}', 
            va='center', ha='left' if v >= 0 else 'right', fontsize=9)
plt.tight_layout()
plt.show()

# =============================================================================
# 4. Segment-Specific Choice Patterns
# =============================================================================

print("\n" + "="*60)
print("SEGMENT-SPECIFIC CHOICE PATTERNS")
print("="*60)

for seg in ['Tech', 'Pragmatist', 'PriceHunter']:
    seg_chosen = chosen_data[chosen_data['Segment'] == seg]
    print(f"\n{seg} (n={len(seg_chosen)} choices):")

    attr_shares = {
        'Range 150': seg_chosen['d_Range_150'].mean(),
        'Price 85K': seg_chosen['d_Price_85'].mean(),
        'Service 300': seg_chosen['d_Service_300'].mean(),
        'Smart Adv': seg_chosen['d_Smart_Adv'].mean(),
        'Warr 6yr': seg_chosen['d_Warr_6'].mean(),
        'Brand Ola': seg_chosen['d_Brand_Ola'].mean(),
        'Brand Honda': seg_chosen['d_Brand_Honda'].mean(),
        'None': seg_chosen['d_None'].mean()
    }
    for attr, share in sorted(attr_shares.items(), key=lambda x: -x[1]):
        print(f"  {attr:12s}: {share:.3f}")

# =============================================================================
# 5. WTP Approximation
# =============================================================================

print("\n" + "="*60)
print("WTP APPROXIMATION")
print("="*60)

# Use log-odds ratio approximation from choice shares
print("Approximate WTP (log-odds ratios from choice shares):")
for attr_col, attr_name in [('d_Range_150', '150km Range'), ('d_Charge_fast', 'Fast Charge'),
                             ('d_Service_300', '300 cities'), ('d_Smart_Adv', 'Advanced Smart'),
                             ('d_Warr_6', '6yr Warranty'), ('d_Brand_Ola', 'Ola Brand'),
                             ('d_Brand_Honda', 'Honda Brand'), ('d_Brand_Ather', 'Ather Brand')]:
    present = chosen_data[chosen_data[attr_col] == 1]
    absent = chosen_data[chosen_data[attr_col] == 0]

    if len(present) > 0 and len(absent) > 0:
        odds_present = present['Chosen'].mean() / (1 - present['Chosen'].mean() + 0.001)
        odds_absent = absent['Chosen'].mean() / (1 - absent['Chosen'].mean() + 0.001)
        oratio = odds_present / odds_absent
        beta_approx = np.log(oratio)
        print(f"  {attr_name:20s}: beta ≈ {beta_approx:6.3f}")

# =============================================================================
# 6. None Rate by Segment
# =============================================================================

print("\n" + "="*60)
print("NONE CHOICE RATE BY SEGMENT")
print("="*60)

none_by_seg = chosen_data.groupby('Segment')['d_None'].mean().sort_values(ascending=False)
print(none_by_seg.round(3))

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(none_by_seg.index, none_by_seg.values * 100, color=['#E37222', '#003366', '#64748b'], edgecolor='white')
ax.set_ylabel('None Choice Rate (%)', fontsize=12)
ax.set_title('"None of These" Choice Rate by Segment', fontsize=13, color='#003366')
for bar, val in zip(bars, none_by_seg.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
            f'{val*100:.1f}%', ha='center', fontsize=11)
plt.tight_layout()
plt.show()

# =============================================================================
# 7. Scribble Pause Box
# =============================================================================

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
    <h3>Pause and Reflect: Metric vs. CBC Agreement</h3>
    <p>The metric conjoint gave you part-worths from ratings. The CBC gives you choice probabilities under competition. Do they tell the same story?</p>
    <table class="scribble-table">
      <thead>
        <tr><th>Question</th><th>Metric Conjoint Said</th><th>CBC Says</th><th>Agree?</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>Most important attribute for Tech</td>
          <td><textarea placeholder="e.g., Smart features..."></textarea></td>
          <td><textarea placeholder="Look at segment-specific choice shares above..."></textarea></td>
          <td><textarea placeholder="Yes / No / Partially..."></textarea></td>
        </tr>
        <tr>
          <td>Most important attribute for Pragmatist</td>
          <td><textarea placeholder="e.g., Service..."></textarea></td>
          <td><textarea placeholder="..."></textarea></td>
          <td><textarea placeholder="..."></textarea></td>
        </tr>
        <tr>
          <td>Why does PriceHunter choose "None" most?</td>
          <td><textarea placeholder="e.g., Low price sensitivity in ratings..."></textarea></td>
          <td><textarea placeholder="e.g., All alternatives too expensive..."></textarea></td>
          <td><textarea placeholder="..."></textarea></td>
        </tr>
      </tbody>
    </table>
    <p style="margin-top:12px;"><strong>Insight:</strong> Where metric and CBC diverge, the CBC is usually more trustworthy — it simulates real competitive choice, not just stated preference.</p>
  </div>
</div>
"""))
