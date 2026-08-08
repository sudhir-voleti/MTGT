# ═══════════════════════════════════════════════════════════════════
#  STEP 4: CBC Analysis — MNL Estimation + WTP
# ═══════════════════════════════════════════════════════════════════

# --- 1. Prepare CBC data for MNL ---
print("="*60)
print("CBC DATA PREP")
print("="*60)

# Create long-format with dummy variables
cbc_long = cbc_df.copy()

# Yana attribute dummies (None = reference for all)
cbc_long['d_Range_110'] = (cbc_long['Range'] == '110km').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_Range_150'] = (cbc_long['Range'] == '150km').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_Charge_fast'] = (cbc_long['Charge'] == '1.5hrs').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_Price_85'] = (cbc_long['Price'] == '85K').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_Price_110'] = (cbc_long['Price'] == '110K').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_Service_100'] = (cbc_long['Service'] == '100cities').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_Service_300'] = (cbc_long['Service'] == '300cities').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_Smart_Adv'] = (cbc_long['Smart'] == 'Advanced').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_Warr_4'] = (cbc_long['Warranty'] == '4yr').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_Warr_6'] = (cbc_long['Warranty'] == '6yr').astype(int) * (cbc_long['AltID'] != 4)
cbc_long['d_None'] = (cbc_long['AltID'] == 4).astype(int)

# --- 2. Aggregate MNL via Logistic Regression ---
print("\n" + "="*60)
print("AGGREGATE MNL (Logistic Regression)")
print("="*60)

from sklearn.linear_model import LogisticRegression

X_cbc = cbc_long[['d_Range_110', 'd_Range_150', 'd_Charge_fast',
                  'd_Price_85', 'd_Price_110',
                  'd_Service_100', 'd_Service_300',
                  'd_Smart_Adv', 'd_Warr_4', 'd_Warr_6', 'd_None']].values
y_cbc = cbc_long['Chosen'].values

# Sample weights to approximate conditional logit (1/number of alts per task)
task_counts = cbc_long.groupby(['RespID', 'Task']).size().reset_index(name='n_alts')
cbc_long = cbc_long.merge(task_counts, on=['RespID', 'Task'])
sample_weights = 1.0 / cbc_long['n_alts']

mnl_agg = LogisticRegression(max_iter=1000, solver='lbfgs')
mnl_agg.fit(X_cbc, y_cbc, sample_weight=sample_weights)

print("Aggregate MNL coefficients:")
for col, coef in zip(['Range_110', 'Range_150', 'Charge_fast', 'Price_85', 'Price_110',
                      'Service_100', 'Service_300', 'Smart_Adv', 'Warr_4', 'Warr_6', 'None'],
                     mnl_agg.coef_[0]):
    print(f"  {col:15s}: {coef:7.3f}")

# --- 3. WTP Computation ---
print("\n" + "="*60)
print("WILLINGNESS TO PAY (WTP)")
print("="*60)

beta_price = abs(mnl_agg.coef_[0][4])  # Price_110 coefficient magnitude
# Use Price_85 as reference for scale
beta_price_ref = abs(mnl_agg.coef_[0][3])

wtp = {}
for name, coef in zip(['Range_110', 'Range_150', 'Charge_fast', 'Service_100', 'Service_300', 'Smart_Adv', 'Warr_4', 'Warr_6'],
                      mnl_agg.coef_[0][:8]):
    if beta_price > 0:
        wtp[name] = -coef / beta_price * 25000  # Rough INR scaling (110K-85K = 25K)
    else:
        wtp[name] = np.nan

print("Approximate WTP (INR vs 140K baseline):")
for name, val in wtp.items():
    if not np.isnan(val):
        print(f"  {name:15s}: ₹{val:,.0f}")

# --- 4. Segment-Specific MNL ---
print("\n" + "="*60)
print("SEGMENT-SPECIFIC MNL")
print("="*60)

# Merge cluster labels
resp_clusters = ib_df[['RespID', 'ClusterName']].copy()
resp_clusters['RespID'] = resp_clusters['RespID'].astype(int)
cbc_seg = cbc_long.merge(resp_clusters, on='RespID', how='left')

for seg in cbc_seg['ClusterName'].dropna().unique():
    seg_data = cbc_seg[cbc_seg['ClusterName'] == seg]
    X_seg = seg_data[['d_Range_110', 'd_Range_150', 'd_Charge_fast',
                      'd_Price_85', 'd_Price_110',
                      'd_Service_100', 'd_Service_300',
                      'd_Smart_Adv', 'd_Warr_4', 'd_Warr_6', 'd_None']].values
    y_seg = seg_data['Chosen'].values
    w_seg = 1.0 / seg_data['n_alts']
    
    mnl_seg = LogisticRegression(max_iter=1000, solver='lbfgs')
    mnl_seg.fit(X_seg, y_seg, sample_weight=w_seg)
    
    print(f"\n{seg}:")
    for col, coef in zip(['Range_110', 'Range_150', 'Charge_fast', 'Price_85', 'Price_110',
                          'Service_100', 'Service_300', 'Smart_Adv', 'Warr_4', 'Warr_6'],
                         mnl_seg.coef_[0][:10]):
        print(f"  {col:15s}: {coef:7.3f}")

print("\n✅ MNL models stored for Step 5 (Market Simulator)")
