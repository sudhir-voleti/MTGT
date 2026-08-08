# ═══════════════════════════════════════════════════════════════════
#  STEP 6: Interactive Configuration Builder
# ═══════════════════════════════════════════════════════════════════

# --- Widgets for Yana configuration ---
sel_range = widgets.Dropdown(options=['75km', '110km', '150km'], value='110km', description='Range:')
sel_charge = widgets.Dropdown(options=['4hrs', '1.5hrs'], value='4hrs', description='Charge:')
sel_price = widgets.Dropdown(options=['85K', '110K', '140K'], value='110K', description='Price:')
sel_service = widgets.Dropdown(options=['25cities', '100cities', '300cities'], value='300cities', description='Service:')
sel_smart = widgets.Dropdown(options=['Basic', 'Advanced'], value='Basic', description='Smart:')
sel_warranty = widgets.Dropdown(options=['2yr', '4yr', '6yr'], value='4yr', description='Warranty:')

btn_simulate = widgets.Button(description='▶ Simulate', button_style='primary')
out_results = widgets.Output()

def on_simulate(_):
    with out_results:
        clear_output()
        
        cfg = {
            'Range': sel_range.value,
            'Charge': sel_charge.value,
            'Price': sel_price.value,
            'Service': sel_service.value,
            'Smart': sel_smart.value,
            'Warranty': sel_warranty.value
        }
        
        # Simulate
        probs = simulate_share(cfg, competitors, mnl_agg)
        t = compute_traction(cfg, mnl_agg)
        clv = project_clv(cfg, competitors, mnl_agg)
        
        print("="*60)
        print("YANA CONFIGURATION")
        print("="*60)
        for k, v in cfg.items():
            print(f"  {k:12s}: {v}")
        
        print("\n" + "="*60)
        print("PREDICTED MARKET SHARE")
        print("="*60)
        for name, p in sorted(probs.items(), key=lambda x: -x[1]):
            marker = "  <<< YANA" if name == 'Yana' else ""
            print(f"  {name:20s}: {p:.1%}{marker}")
        
        print("\n" + "="*60)
        print("TRACTION DIAGNOSIS")
        print("="*60)
        print(f"  V (Value)     : {t['V']:.3f}")
        print(f"  A (Access)    : {t['A']:.3f}")
        print(f"  E (Evidence)  : {t['E']:.3f}")
        print(f"  Traction      : {t['Traction']:.3f}")
        
        print("\n" + "="*60)
        print("CLV PROJECTION")
        print("="*60)
        print(f"  Market Share  : {clv['Market_Share']:.1%}")
        print(f"  CLV per Unit  : ₹{clv['CLV']:,.0f}")
        
        # Plot
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        
        # Share bar chart
        ax = axes[0]
        names = list(probs.keys())
        vals = [probs[n] for n in names]
        colors = ['#2c7a7b' if n == 'Yana' else '#718096' for n in names]
        ax.barh(names, vals, color=colors, edgecolor='black')
        ax.set_xlabel('Choice Probability')
        ax.set_title('Market Share Simulation')
        ax.set_xlim(0, max(vals) * 1.2)
        
        # Traction pillars
        ax = axes[1]
        pillars = ['V\n(Value)', 'A\n(Access)', 'E\n(Evidence)']
        pvals = [t['V'], t['A'], t['E']]
        pcolors = ['#2c7a7b', '#d69e2e', '#e53e3e']
        ax.bar(pillars, pvals, color=pcolors, edgecolor='black')
        ax.set_ylabel('Score (0-1)')
        ax.set_title(f'Traction = {t["Traction"]:.3f}')
        ax.set_ylim(0, 1.05)
        
        plt.tight_layout()
        plt.show()

btn_simulate.on_click(on_simulate)

ui = widgets.VBox([
    widgets.HTML("<h2>Step 6: Yana Configuration Simulator</h2>"),
    widgets.HTML("<p>Build a Yana SKU and see predicted share, traction, and CLV.</p>"),
    widgets.HBox([sel_range, sel_charge, sel_price]),
    widgets.HBox([sel_service, sel_smart, sel_warranty]),
    btn_simulate,
    out_results
])

display(ui)
