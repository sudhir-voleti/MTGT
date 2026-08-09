# -*- coding: utf-8 -*-
"""
Lec09 — Step 3: Individual-Level OLS + K-Means Clustering
Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/03_individual_ols.py').text)
Prerequisite: 02_upload.py should have been run (metric_df in globals).
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

# =============================================================================
# 1. Retrieve or re-upload data
# =============================================================================

if 'metric_df' in globals():
    metric_df = globals()['metric_df']
    print("✓ Using metric_df from previous cell")
else:
    print("⚠ metric_df not found. Please upload yana_metric_conjoint_n400.csv below:")
    upload_widget = widgets.FileUpload(accept='.csv', multiple=False, description='Upload CSV')
    def _load(change):
        if len(upload_widget.value) > 0:
            content = upload_widget.value[0]['content']
            with open('/tmp/metric.csv', 'wb') as f:
                f.write(content)
            globals()['metric_df'] = pd.read_csv('/tmp/metric.csv')
            print("✓ Loaded")
    upload_widget.observe(_load, names='value')
    display(upload_widget)
    raise SystemExit("Re-run this cell after uploading")

# =============================================================================
# 2. Individual-Level OLS
# =============================================================================

print("\n" + "="*60)
print("INDIVIDUAL-LEVEL OLS: Estimating Part-Worths")
print("="*60)
print("Running one regression per respondent (400 models)...")

individual_betas = []

for resp_id in metric_df['RespID'].unique():
    resp_data = metric_df[metric_df['RespID'] == resp_id].copy()

    # Create dummies
    resp_data['d_Range_110'] = (resp_data['Range'] == '110km').astype(int)
    resp_data['d_Range_150'] = (resp_data['Range'] == '150km').astype(int)
    resp_data['d_Charge_fast'] = (resp_data['Charge'] == '1.5hrs').astype(int)
    resp_data['d_Price_85'] = (resp_data['Price'] == '85K').astype(int)
    resp_data['d_Price_110'] = (resp_data['Price'] == '110K').astype(int)
    resp_data['d_Service_100'] = (resp_data['Service'] == '100cities').astype(int)
    resp_data['d_Service_300'] = (resp_data['Service'] == '300cities').astype(int)
    resp_data['d_Smart_Adv'] = (resp_data['Smart'] == 'Advanced').astype(int)
    resp_data['d_Warr_4'] = (resp_data['Warranty'] == '4yr').astype(int)
    resp_data['d_Warr_6'] = (resp_data['Warranty'] == '6yr').astype(int)
    resp_data['d_Brand_Honda'] = (resp_data['Brand'] == 'Honda').astype(int)
    resp_data['d_Brand_Ola'] = (resp_data['Brand'] == 'Ola').astype(int)
    resp_data['d_Brand_Ather'] = (resp_data['Brand'] == 'Ather').astype(int)

    Xi = resp_data[['d_Range_110', 'd_Range_150', 'd_Charge_fast',
                    'd_Price_85', 'd_Price_110',
                    'd_Service_100', 'd_Service_300',
                    'd_Smart_Adv', 'd_Warr_4', 'd_Warr_6',
                    'd_Brand_Honda', 'd_Brand_Ola', 'd_Brand_Ather']]
    Xi = sm.add_constant(Xi)
    yi = resp_data['Rating']

    try:
        mi = sm.OLS(yi, Xi).fit()
        individual_betas.append({
            'RespID': resp_id,
            'Segment': resp_data['Segment'].iloc[0],
            'Intercept': mi.params.get('const', np.nan),
            'Range_110': mi.params.get('d_Range_110', np.nan),
            'Range_150': mi.params.get('d_Range_150', np.nan),
            'Charge_fast': mi.params.get('d_Charge_fast', np.nan),
            'Price_85': mi.params.get('d_Price_85', np.nan),
            'Price_110': mi.params.get('d_Price_110', np.nan),
            'Service_100': mi.params.get('d_Service_100', np.nan),
            'Service_300': mi.params.get('d_Service_300', np.nan),
            'Smart_Adv': mi.params.get('d_Smart_Adv', np.nan),
            'Warr_4': mi.params.get('d_Warr_4', np.nan),
            'Warr_6': mi.params.get('d_Warr_6', np.nan),
            'Brand_Honda': mi.params.get('d_Brand_Honda', np.nan),
            'Brand_Ola': mi.params.get('d_Brand_Ola', np.nan),
            'Brand_Ather': mi.params.get('d_Brand_Ather', np.nan)
        })
    except:
        pass

ib_df = pd.DataFrame(individual_betas)
print(f"✓ Individual models estimated: {len(ib_df)} / {metric_df['RespID'].nunique()}")

# Store for next cells
globals()['ib_df'] = ib_df

# =============================================================================
# 3. Attribute Importance
# =============================================================================

print("\n" + "="*60)
print("ATTRIBUTE IMPORTANCE")
print("="*60)

def compute_importance(row):
    range_pw = [0, row['Range_110'], row['Range_150']]
    range_imp = max(range_pw) - min(range_pw)

    charge_pw = [0, row['Charge_fast']]
    charge_imp = max(charge_pw) - min(charge_pw)

    price_pw = [0, row['Price_85'], row['Price_110']]
    price_imp = max(price_pw) - min(price_pw)

    service_pw = [0, row['Service_100'], row['Service_300']]
    service_imp = max(service_pw) - min(service_pw)

    smart_pw = [0, row['Smart_Adv']]
    smart_imp = max(smart_pw) - min(smart_pw)

    warr_pw = [0, row['Warr_4'], row['Warr_6']]
    warr_imp = max(warr_pw) - min(warr_pw)

    brand_pw = [0, row['Brand_Honda'], row['Brand_Ola'], row['Brand_Ather']]
    brand_imp = max(brand_pw) - min(brand_pw)

    total = range_imp + charge_imp + price_imp + service_imp + smart_imp + warr_imp + brand_imp
    if total == 0:
        return pd.Series([np.nan]*7)

    return pd.Series([
        range_imp/total*100, charge_imp/total*100, price_imp/total*100,
        service_imp/total*100, smart_imp/total*100, warr_imp/total*100,
        brand_imp/total*100
    ], index=['Range', 'Charge', 'Price', 'Service', 'Smart', 'Warranty', 'Brand'])

importance = ib_df.apply(compute_importance, axis=1)
importance['RespID'] = ib_df['RespID']
importance['Segment'] = ib_df['Segment']

imp_overall = importance[['Range','Charge','Price','Service','Smart','Warranty','Brand']].mean()
print("\nOverall attribute importance (%):")
print(imp_overall.round(1).sort_values(ascending=False))

imp_by_seg = importance.groupby('Segment')[['Range','Charge','Price','Service','Smart','Warranty','Brand']].mean()
print("\nAttribute importance by segment (%):")
print(imp_by_seg.round(1))

# Bar chart
fig, ax = plt.subplots(figsize=(10, 5))
imp_overall_sorted = imp_overall.sort_values(ascending=True)
colors = ['#E37222' if v == imp_overall_sorted.max() else '#003366' for v in imp_overall_sorted]
ax.barh(imp_overall_sorted.index, imp_overall_sorted.values, color=colors, edgecolor='white')
ax.set_xlabel('Importance (%)', fontsize=12)
ax.set_title('Overall Attribute Importance', fontsize=13, color='#003366')
for i, v in enumerate(imp_overall_sorted.values):
    ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=10)
plt.tight_layout()
plt.show()

# Store
globals()['importance'] = importance

# =============================================================================
# 4. K-Means Clustering
# =============================================================================

print("\n" + "="*60)
print("K-MEANS CLUSTERING ON PART-WORTHS")
print("="*60)

pw_matrix = ib_df[['Range_110', 'Range_150', 'Charge_fast', 'Price_85', 'Price_110',
                   'Service_100', 'Service_300', 'Smart_Adv', 'Warr_4', 'Warr_6',
                   'Brand_Honda', 'Brand_Ola', 'Brand_Ather']].fillna(0)
scaler = StandardScaler()
pw_scaled = scaler.fit_transform(pw_matrix)

# Try K=2,3,4 and show inertia
print("\nInertia (within-cluster sum of squares):")
for k in [2, 3, 4]:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(pw_scaled)
    print(f"  K={k}: {km.inertia_:.1f}")

# Use K=3 (known ground truth)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(pw_scaled)
ib_df['Cluster'] = clusters

print("\nCluster x True Segment cross-tab:")
cluster_seg = pd.crosstab(ib_df['Cluster'], ib_df['Segment'])
print(cluster_seg)

print("\nCluster purity:")
for seg in ['Tech', 'Pragmatist', 'PriceHunter']:
    seg_clusters = ib_df[ib_df['Segment'] == seg]['Cluster']
    vc = seg_clusters.value_counts()
    purity = vc.iloc[0] / len(seg_clusters) * 100
    print(f"  {seg:12s}: {purity:5.1f}% in Cluster {vc.index[0]}")

# Cluster profiles (mean part-worths)
print("\nCluster profiles (mean part-worths):")
cluster_profiles = ib_df.groupby('Cluster')[['Range_110', 'Range_150', 'Charge_fast',
                                                'Price_85', 'Price_110',
                                                'Service_100', 'Service_300',
                                                'Smart_Adv', 'Warr_4', 'Warr_6',
                                                'Brand_Honda', 'Brand_Ola', 'Brand_Ather']].mean()
print(cluster_profiles.round(2))

# Store
globals()['cluster_profiles'] = cluster_profiles

# =============================================================================
# 5. Scribble Pause Box
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
    <h3>Pause and Reflect: Did the Clusters Match Your Intuition?</h3>
    <p>Look at the cluster profiles above. Can you map each cluster to a segment name?</p>
    <table class="scribble-table">
      <thead>
        <tr><th>Cluster</th><th>My Segment Name</th><th>What this cluster values most</th></tr>
      </thead>
      <tbody>
        <tr><td>Cluster 0</td><td><textarea placeholder="e.g., Pragmatist..."></textarea></td>
            <td><textarea placeholder="e.g., Service + Honda brand..."></textarea></td></tr>
        <tr><td>Cluster 1</td><td><textarea placeholder="e.g., Tech..."></textarea></td>
            <td><textarea placeholder="e.g., Smart + Ola brand..."></textarea></td></tr>
        <tr><td>Cluster 2</td><td><textarea placeholder="e.g., PriceHunter..."></textarea></td>
            <td><textarea placeholder="e.g., Low price..."></textarea></td></tr>
      </tbody>
    </table>
    <p style="margin-top:12px;"><strong>Compare:</strong> Look back at Prediction 3 from the theory section. How many segments did you predict? Did you get the defining attributes right?</p>
  </div>
</div>
"""))
