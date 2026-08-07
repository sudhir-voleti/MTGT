"""Chunk 4: Map items to Whole Product layers and find the gap."""

if 'df' not in globals():
    raise RuntimeError("Run Chunk 1 first!")

# --- Layer Selectors ---
sel_l1 = widgets.SelectMultiple(description='L1 Generic', options=item_cols, rows=6,
    value=tuple(c for c in item_cols if any(k in c.lower() for k in ['pioneer','drive','data.hunger','risk.tol','social'])),
    layout=widgets.Layout(width='220px'))
sel_l2 = widgets.SelectMultiple(description='L2 Expected', options=item_cols, rows=6,
    value=tuple(c for c in item_cols if any(k in c.lower() for k in ['privacy','accuracy','stigma'])),
    layout=widgets.Layout(width='220px'))
sel_l3a = widgets.SelectMultiple(description='L3a Evidence', options=item_cols, rows=6,
    value=tuple(c for c in item_cols if any(k in c.lower() for k in ['compliance','clinical'])),
    layout=widgets.Layout(width='220px'))
sel_l3b = widgets.SelectMultiple(description='L3b Access', options=item_cols, rows=6,
    value=tuple(c for c in item_cols if any(k in c.lower() for k in ['integration','simplicity','support'])),
    layout=widgets.Layout(width='220px'))

btn_lock = widgets.Button(description='🔒 Lock Layers', button_style='success')
out = widgets.Output()

def lock_and_diagnose(_):
    global wp_map
    with out:
        clear_output()
        
        l1, l2, l3a, l3b = list(sel_l1.value), list(sel_l2.value), list(sel_l3a.value), list(sel_l3b.value)
        wp_map = {'L1':l1, 'L2':l2, 'L3a':l3a, 'L3b':l3b}
        
        # Compute layer scores
        for name, cols in wp_map.items():
            df[f'{name}_score'] = df[cols].apply(lambda x: normalize(x).mean(), axis=1) if cols else 0.0
        
        # Segment summary
        levels = ['L1_score','L2_score','L3a_score','L3b_score']
        seg = df.groupby(seg_col)[levels].mean().reset_index()
        seg['Moore'] = seg[seg_col].map(moore_map)
        seg['n'] = seg[seg_col].map(df[seg_col].value_counts())
        seg['%'] = (seg['n']/len(df)*100).round(1)
        
        # Gap detection
        def find_gap(row):
            for i, lv in enumerate(levels):
                if row[lv] >= 0.50:
                    if i == len(levels)-1: return "None"
                    nxt = levels[i+1]
                    if row[nxt] < 0.40: return nxt.replace('_score','')
            return "No Core Demand"
        seg['Gap'] = seg.apply(find_gap, axis=1)
        
        print("📊 Whole Product Layer Scores & Gaps\n")
        display(seg[['seg_col','Moore','L1_score','L2_score','L3a_score','L3b_score','Gap','n','%']].round(3))
        
        # Plot
        fig, axes = plt.subplots(1,2, figsize=(14,5))
        
        # A: Layer profiles
        ax = axes[0]
        x = np.arange(len(seg)); w=0.2
        colors = ['#2c7a7b','#718096','#d69e2e','#e53e3e']
        for i, (lv,name) in enumerate(zip(levels, ['L1','L2','L3a','L3b'])):
            ax.bar(x+i*w, seg[lv], w, label=name, color=colors[i], edgecolor='black')
        ax.axhline(0.50, color='red', linestyle='--', alpha=0.6)
        ax.set_xticks(x+1.5*w); ax.set_xticklabels(seg[seg_col], rotation=15, ha='right')
        ax.set_ylabel('Score'); ax.set_title('Whole Product Demand by Segment'); ax.legend(); ax.set_ylim(0,1.05)
        
        # B: Chasm Readiness
        ax = axes[1]
        for _, r in seg.iterrows():
            x_val = r['L1_score']
            y_val = (r['L3a_score'] + r['L3b_score'])/2
            ax.scatter(x_val, y_val, s=r['n']*4, alpha=0.7, edgecolors='black')
            ax.annotate(r[seg_col], (x_val, y_val), xytext=(5,5), fontsize=9, fontweight='bold')
        ax.axvline(0.50, color='gray', linestyle='--'); ax.axhline(0.50, color='gray', linestyle='--')
        ax.text(0.25,0.75,'Chasm\n(High Demand,\nLow Supply)', ha='center', color='red', fontweight='bold')
        ax.text(0.75,0.75,'Whole Product\nReady', ha='center', color='green', fontweight='bold')
        ax.set_xlabel('L1 Generic (Supply)'); ax.set_ylabel('(L3a + L3b)/2 (Demand)')
        ax.set_title('Chasm Readiness Map'); ax.set_xlim(0,1); ax.set_ylim(0,1)
        
        plt.tight_layout(); plt.show()

btn_lock.on_click(lock_and_diagnose)

display(widgets.VBox([
    widgets.HTML("<h2>Step 4: Whole Product Gap Analysis</h2>"),
    widgets.HTML("<p>Moore says you need 4 layers to cross the chasm. Where is Hridayam missing?</p>"),
    widgets.HBox([sel_l1, sel_l2, sel_l3a, sel_l3b]),
    btn_lock,
    out
]))
