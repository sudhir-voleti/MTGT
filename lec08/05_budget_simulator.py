"""Chunk 5: The $3M Board Meeting. Build product configs and see which crosses the chasm."""

BUDGET = 3_000_000

# Feature inventory: (name, level, cost)
FEATURES = [
    ("ECG Patch + App + Portal", "L1", 0),
    ("Basic Privacy", "L2", 0),
    ("HIPAA/GDPR Cert", "L2", 400_000),
    ("FDA 510(k)", "L3a", 2_000_000),
    ("Peer-Reviewed Study", "L3a", 800_000),
    ("IT Integration API", "L3b", 200_000),
    ("24/7 Support Desk", "L3b", 150_000),
    ("B2B Procurement Portal", "L3b", 100_000),
]

# Build checkboxes
feature_cbs = {}
for name, lvl, cost in FEATURES:
    cb = widgets.Checkbox(
        value=(cost==0), 
        description=f"{name} (${cost:,})" if cost else f"{name} (Sunk)",
        disabled=(cost==0),
        layout=widgets.Layout(width='350px')
    )
    feature_cbs[name] = (cb, lvl, cost)

# Budget bar
budget_html = widgets.HTML()

def update_budget():
    cost = sum(c for _,(cb,lvl,c) in feature_cbs.items() if cb.value and not cb.disabled)
    pct = cost/BUDGET*100
    color = "#2c7a7b" if cost<=BUDGET else "#c53030"
    bar = "█" * int(pct/5) + "░" * (20 - int(pct/5))
    budget_html.value = f"<h3 style='color:{color}'>Budget: ${cost:,} / ${BUDGET:,} {bar} ({pct:.0f}%)</h3>"

for cb,_,_ in feature_cbs.values():
    cb.observe(lambda ch: update_budget(), names='value')

txt_name = widgets.Text(value="My Config", description="Name:")
btn_save = widgets.Button(description='💾 Save Config', button_style='success')
btn_compare = widgets.Button(description='▶ Compare All', button_style='primary')
out = widgets.Output()

saved_configs = []

def save_config(_):
    with out:
        clear_output()
        cost = sum(c for _,(cb,lvl,c) in feature_cbs.items() if cb.value and not cb.disabled)
        if cost > BUDGET:
            print(f"❌ Over budget by ${cost-BUDGET:,}!"); return
        
        levels = set(lvl for _,(cb,lvl,c) in feature_cbs.items() if cb.value)
        cfg = {"name": txt_name.value, "cost": cost, "levels": levels,
               "features": [n for n,(cb,l,c) in feature_cbs.items() if cb.value]}
        saved_configs.append(cfg)
        print(f"✅ Saved '{cfg['name']}' | ${cost:,} | Levels: {', '.join(levels)}")

def compare(_):
    with out:
        clear_output()
        if not saved_configs:
            print("Save at least one config first."); return
        
        # Need traction scores from Chunk 3
        if 'V_score' not in df.columns:
            print("❌ Run Chunk 3 (Traction) first!"); return
        
        # Compute traction for each config
        results = []
        for cfg in saved_configs:
            has_l3b = 'L3b' in cfg['levels']
            has_l3a = 'L3a' in cfg['levels']
            has_l2 = 'L2' in cfg['levels']
            
            # Apply multipliers
            df['A_eff'] = df['A_score'] * (1.0 if has_l3b else (0.85 if has_l2 else 0.7))
            df['E_eff'] = df['E_score'] * (1.0 if has_l3a else (0.85 if has_l2 else 0.7))
            df['traction_cfg'] = df['V_score'] * df['A_eff'] * df['E_eff']
            
            agg = df.groupby(seg_col)['traction_cfg'].mean().reset_index()
            agg['config'] = cfg['name']
            agg['cost'] = cfg['cost']
            agg['Moore'] = agg[seg_col].map(moore_map)
            results.append(agg)
        
        res_df = pd.concat(results)
        
        # Plot Chasm Cliff
        fig, ax = plt.subplots(figsize=(10,6))
        moore_order = ['Innovators','Early Adopters','Early Majority','Late Majority','Laggards']
        
        for i, cfg in enumerate(saved_configs):
            sub = res_df[res_df['config']==cfg['name']].set_index('Moore').reindex(moore_order)
            ax.plot(moore_order, sub['traction_cfg'], marker='o', label=f"{cfg['name']} (${cfg['cost']:,})")
        
        ax.axvspan(0.7, 1.3, alpha=0.1, color='red', label='Chasm Zone')
        ax.set_title('Chasm Cliff: Traction by Moore Category')
        ax.set_ylabel('Mean Traction'); ax.legend(loc='upper left')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')
        plt.tight_layout(); plt.show()
        
        # Find best for Pragmatists
        prag = res_df[res_df['Moore']=='Early Majority']
        if not prag.empty:
            best = prag.loc[prag['traction_cfg'].idxmax()]
            print(f"\n🏆 Best for Pragmatists: {best['config']} with traction={best['traction_cfg']:.3f}")

btn_save.on_click(save_config)
btn_compare.on_click(compare)

update_budget()

display(widgets.VBox([
    widgets.HTML("<h2>Step 5: The Board Meeting — $3M Budget Simulator</h2>"),
    widgets.HTML("<p>Check features to build. Watch the budget bar. Save configs. Compare.</p>"),
    budget_html,
    widgets.VBox([cb for cb,_,_ in feature_cbs.values()]),
    widgets.HBox([txt_name, btn_save, btn_compare]),
    out
]))
