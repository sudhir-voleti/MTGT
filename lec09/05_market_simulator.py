# ═══════════════════════════════════════════════════════════════════
#  STEP 5: Market Simulator — Share Prediction + Traction + CLV
# ═══════════════════════════════════════════════════════════════════

# --- 1. Define competitive scenarios ---
print("="*60)
print("MARKET SIMULATOR")
print("="*60)

# Competitor definitions (as dictionaries)
competitors = {
    'Honda_Activa_e': {'Range': '85km', 'Charge': '4hrs', 'Price': '95K', 
                       'Service': '300cities', 'Smart': 'Basic', 'Warranty': '2yr'},
    'Ola_S1_Pro':     {'Range': '120km', 'Charge': '1.5hrs', 'Price': '125K',
                       'Service': '100cities', 'Smart': 'Advanced', 'Warranty': '2yr'},
    'Ather_450X':     {'Range': '110km', 'Charge': '1.5hrs', 'Price': '135K',
                       'Service': '25cities', 'Smart': 'Advanced', 'Warranty': '2yr'}
}

# Yana candidate configurations
yana_configs = {
    'S1_Current':     {'Range': '150km', 'Charge': '1.5hrs', 'Price': '140K',
                      'Service': '25cities', 'Smart': 'Advanced', 'Warranty': '4yr'},
    'Pragmatist_SKU': {'Range': '110km', 'Charge': '4hrs', 'Price': '110K',
                       'Service': '300cities', 'Smart': 'Basic', 'Warranty': '4yr'},
    'Budget_SKU':     {'Range': '75km', 'Charge': '4hrs', 'Price': '85K',
                       'Service': '300cities', 'Smart': 'Basic', 'Warranty': '2yr'}
}

# --- 2. Compute utilities for any configuration ---
def config_to_dummies(cfg):
    """Convert config dict to dummy vector matching MNL input."""
    d = np.zeros(10)
    # Range
    if cfg['Range'] == '110km': d[0] = 1
    elif cfg['Range'] == '150km': d[1] = 1
    # Charge
    if cfg['Charge'] == '1.5hrs': d[2] = 1
    # Price
    if cfg['Price'] == '85K': d[3] = 1
    elif cfg['Price'] == '110K': d[4] = 1
    # Service
    if cfg['Service'] == '100cities': d[5] = 1
    elif cfg['Service'] == '300cities': d[6] = 1
    # Smart
    if cfg['Smart'] == 'Advanced': d[7] = 1
    # Warranty
    if cfg['Warranty'] == '4yr': d[8] = 1
    elif cfg['Warranty'] == '6yr': d[9] = 1
    return d

# --- 3. Simulate market share ---
def simulate_share(yana_cfg, competitors_dict, mnl_model, segment_weights=None):
    """Compute Yana's predicted choice share."""
    
    # Build choice set: Yana + competitors + None
    all_products = {'Yana': yana_cfg}
    all_products.update(competitors_dict)
    
    utilities = {}
    for name, cfg in all_products.items():
        d = config_to_dummies(cfg)
        u = mnl_model.coef_[0][:10].dot(d) + mnl_model.intercept_[0]
        utilities[name] = u
    
    # None utility
    utilities['None'] = mnl_model.coef_[0][10] if len(mnl_model.coef_[0]) > 10 else -1.0
    
    # Logit probabilities
    exp_u = {k: np.exp(v) for k, v in utilities.items()}
    total = sum(exp_u.values())
    probs = {k: v/total for k, v in exp_u.items()}
    
    return probs

# --- 4. Run simulations ---
print("\n--- Scenario: Pragmatist SKU vs Competitors ---")
probs = simulate_share(yana_configs['Pragmatist_SKU'], competitors, mnl_agg)
for name, p in sorted(probs.items(), key=lambda x: -x[1]):
    print(f"  {name:20s}: {p:.1%}")

print("\n--- Scenario: S1 Current vs Competitors ---")
probs2 = simulate_share(yana_configs['S1_Current'], competitors, mnl_agg)
for name, p in sorted(probs2.items(), key=lambda x: -x[1]):
    print(f"  {name:20s}: {p:.1%}")

print("\n--- Scenario: Budget SKU vs Competitors ---")
probs3 = simulate_share(yana_configs['Budget_SKU'], competitors, mnl_agg)
for name, p in sorted(probs3.items(), key=lambda x: -x[1]):
    print(f"  {name:20s}: {p:.1%}")

# --- 5. Traction Computation ---
print("\n" + "="*60)
print("TRACTION = V × A × E")
print("="*60)

def compute_traction(cfg, mnl_model):
    """Compute V, A, E pillars from part-worths."""
    d = config_to_dummies(cfg)
    coefs = mnl_model.coef_[0][:10]
    
    # V = Range + Smart
    V = coefs[0]*d[0] + coefs[1]*d[1] + coefs[7]*d[7]
    # A = -Price + Service + Charge (lower price = higher access)
    A = -(coefs[3]*d[3] + coefs[4]*d[4]) + coefs[5]*d[5] + coefs[6]*d[6] + coefs[2]*d[2]
    # E = Warranty
    E = coefs[8]*d[8] + coefs[9]*d[9]
    
    # Normalize to 0-1
    V_norm = 1 / (1 + np.exp(-V))
    A_norm = 1 / (1 + np.exp(-A))
    E_norm = 1 / (1 + np.exp(-E))
    
    traction = V_norm * A_norm * E_norm
    
    return {'V': V_norm, 'A': A_norm, 'E': E_norm, 'Traction': traction}

for name, cfg in yana_configs.items():
    t = compute_traction(cfg, mnl_agg)
    print(f"\n{name}:")
    print(f"  V (Value)     : {t['V']:.3f}")
    print(f"  A (Access)    : {t['A']:.3f}")
    print(f"  E (Evidence)  : {t['E']:.3f}")
    print(f"  Traction (V×A×E): {t['Traction']:.3f}")

# --- 6. CLV Projection ---
print("\n" + "="*60)
print("CLV PROJECTION")
print("="*60)

# Simplified CLV model
def project_clv(yana_cfg, competitors_dict, mnl_model, 
                segment_sizes={'Tech': 0.25, 'Pragmatist': 0.45, 'PriceHunter': 0.30},
                margin_per_unit=15000, cac=5000, ownership_years=5):
    """Project CLV for a Yana configuration."""
    
    total_share = 0
    weighted_traction = 0
    
    for seg_name, seg_weight in segment_sizes.items():
        # Use segment-specific model if available, else aggregate
        seg_data = cbc_seg[cbc_seg['ClusterName'] == seg_name] if 'cbc_seg' in globals() else None
        
        if seg_data is not None and len(seg_data) > 0:
            # Re-fit quick model for this segment
            X_seg = seg_data[['d_Range_110', 'd_Range_150', 'd_Charge_fast',
                              'd_Price_85', 'd_Price_110', 'd_Service_100',
                              'd_Service_300', 'd_Smart_Adv', 'd_Warr_4', 'd_Warr_6', 'd_None']].values
            y_seg = seg_data['Chosen'].values
            w_seg = 1.0 / seg_data['n_alts']
            
            mnl_seg = LogisticRegression(max_iter=1000, solver='lbfgs')
            mnl_seg.fit(X_seg, y_seg, sample_weight=w_seg)
            probs = simulate_share(yana_cfg, competitors_dict, mnl_seg)
        else:
            probs = simulate_share(yana_cfg, competitors_dict, mnl_model)
        
        yana_share = probs.get('Yana', 0)
        total_share += yana_share * seg_weight
        
        t = compute_traction(yana_cfg, mnl_model)
        weighted_traction += t['Traction'] * seg_weight
    
    # CLV = (Share × Margin × Years) − CAC
    clv = total_share * margin_per_unit * ownership_years - cac
    
    return {
        'Market_Share': total_share,
        'Traction': weighted_traction,
        'CLV': clv,
        'Margin_Per_Unit': margin_per_unit,
        'CAC': cac
    }

for name, cfg in yana_configs.items():
    clv = project_clv(cfg, competitors, mnl_agg)
    print(f"\n{name}:")
    print(f"  Market Share: {clv['Market_Share']:.1%}")
    print(f"  Traction:     {clv['Traction']:.3f}")
    print(f"  CLV:          ₹{clv['CLV']:,.0f}")
    print(f"  (Margin: ₹{clv['Margin_Per_Unit']:,}, CAC: ₹{clv['CAC']:,})")

print("\n✅ Simulator ready for scenario testing")
