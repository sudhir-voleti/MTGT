# ═══════════════════════════════════════════════════════════════════
#  STEP 2: Metric Conjoint — Estimate Part-Worths
# ═══════════════════════════════════════════════════════════════════

from sklearn.linear_model import LinearRegression

# --- 1. Create dummy variables ---
dummies = metric_df.copy()

# Reference levels: 75km, 4hrs, 140K, 25cities, Basic, 2yr
dummies['d_Range_110'] = (dummies['Range'] == '110km').astype(int)
dummies['d_Range_150'] = (dummies['Range'] == '150km').astype(int)
dummies['d_Charge_fast'] = (dummies['Charge'] == '1.5hrs').astype(int)
dummies['d_Price_85'] = (dummies['Price'] == '85K').astype(int)
dummies['d_Price_110'] = (dummies['Price'] == '110K').astype(int)
dummies['d_Service_100'] = (dummies['Service'] == '100cities').astype(int)
dummies['d_Service_300'] = (dummies['Service'] == '300cities').astype(int)
dummies['d_Smart_Adv'] = (dummies['Smart'] == 'Advanced').astype(int)
dummies['d_Warr_4'] = (dummies['Warranty'] == '4yr').astype(int)
dummies['d_Warr_6'] = (dummies['Warranty'] == '6yr').astype(int)

X_cols = ['d_Range_110', 'd_Range_150', 'd_Charge_fast',
          'd_Price_85', 'd_Price_110',
          'd_Service_100', 'd_Service_300',
          'd_Smart_Adv', 'd_Warr_4', 'd_Warr_6']

# --- 2. Aggregate OLS ---
print("="*60)
print("AGGREGATE OLS")
print("="*60)

X = dummies[X_cols].values
y = dummies['Rating'].values
agg_model = LinearRegression()
agg_model.fit(X, y)

print(f"Intercept: {agg_model.intercept_:.3f}")
for col, coef in zip(X_cols, agg_model.coef_):
    print(f"{col:20s}: {coef:7.3f}")

# --- 3. Individual-Level OLS ---
print("\n" + "="*60)
print("INDIVIDUAL-LEVEL PART-WORTHS")
print("="*60)

individual_betas = []

for resp_id in metric_df['RespID'].unique():
    resp_data = dummies[dummies['RespID'] == resp_id].copy()
    Xi = resp_data[X_cols].values
    yi = resp_data['Rating'].values
    
    if np.any(Xi.std(axis=0) == 0):
        continue
    
    mi = LinearRegression()
    mi.fit(Xi, yi)
    
    individual_betas.append({
        'RespID': resp_id,
        'Intercept': mi.intercept_,
        'Range_110': mi.coef_[0], 'Range_150': mi.coef_[1],
        'Charge_fast': mi.coef_[2],
        'Price_85': mi.coef_[3], 'Price_110': mi.coef_[4],
        'Service_100': mi.coef_[5], 'Service_300': mi.coef_[6],
        'Smart_Adv': mi.coef_[7],
        'Warr_4': mi.coef_[8], 'Warr_6': mi.coef_[9]
    })

ib_df = pd.DataFrame(individual_betas)
print(f"Estimated: {len(ib_df)} individual models")

# --- 4. Attribute Importance ---
def compute_importance(row):
    range_imp = max(0, row['Range_110'], row['Range_150']) - min(0, row['Range_110'], row['Range_150'])
    charge_imp = max(0, row['Charge_fast']) - min(0, row['Charge_fast'])
    price_imp = max(0, row['Price_85'], row['Price_110']) - min(0, row['Price_85'], row['Price_110'])
    service_imp = max(0, row['Service_100'], row['Service_300']) - min(0, row['Service_100'], row['Service_300'])
    smart_imp = max(0, row['Smart_Adv']) - min(0, row['Smart_Adv'])
    warr_imp = max(0, row['Warr_4'], row['Warr_6']) - min(0, row['Warr_4'], row['Warr_6'])
    
    total = range_imp + charge_imp + price_imp + service_imp + smart_imp + warr_imp
    if total == 0:
        return pd.Series([np.nan]*6)
    
    return pd.Series([
        range_imp/total*100, charge_imp/total*100, price_imp/total*100,
        service_imp/total*100, smart_imp/total*100, warr_imp/total*100
    ], index=['Range', 'Charge', 'Price', 'Service', 'Smart', 'Warranty'])

importance = ib_df.apply(compute_importance, axis=1)
importance['RespID'] = ib_df['RespID']

print("\n--- Mean Attribute Importance ---")
print(importance.mean().round(1))

# Store for next step
ib_df['RespID'] = ib_df['RespID'].astype(int)
print("\n✅ Part-worths stored in ib_df for Step 3 (Segmentation)")
