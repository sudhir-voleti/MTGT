"""Chunk 3: Compute V × A × E and diagnose the chasm."""

# --- FORMULA (shown in markdown above this cell in your notebook) ---
# Traction = V × A × E
# V = mean of VALUE items (what they want)
# A = mean of ACCESS items (how easy to get)
# E = mean of EVIDENCE items (proof/trust)

if 'df' not in globals() or 'moore_map' not in globals():
    raise RuntimeError("Run Chunks 1 & 2 first!")

# --- V|A|E Item Selectors ---
all_items = item_cols  # from Chunk 1

sel_v = widgets.SelectMultiple(description='VALUE', options=all_items, rows=6,
    value=tuple(c for c in all_items if any(k in c.lower() for k in ['pioneer','drive','data.hunger','risk.tol','social'])),
    layout=widgets.Layout(width='260px'))
sel_a = widgets.SelectMultiple(description='ACCESS', options=all_items, rows=6,
    value=tuple(c for c in all_items if any(k in c.lower() for k in ['integration','simplicity','support'])),
    layout=widgets.Layout(width='260px'))
sel_e = widgets.SelectMultiple(description='EVIDENCE', options=all_items, rows=6,
    value=tuple(c for c in all_items if any(k in c.lower() for k in ['compliance','clinical','privacy','accuracy','stigma'])),
    layout=widgets.Layout(width='260px'))

btn_run = widgets.Button(description='▶ Compute Traction', button_style='primary')
out = widgets.Output()

def compute(_):
    with out:
        clear_output()
        
        v_items = list(sel_v.value)
        a_items = list(sel_a.value)
        e_items = list(sel_e.value)
        
        if not (v_items and a_items and e_items):
            print("❌ Select at least one item for each pillar.")
            return
        
        # Normalize and compute
        df['V_score'] = df[v_items].apply(lambda x: normalize(x).mean(), axis=1)
        df['A_score'] = df[a_items].apply(lambda x: normalize(x).mean(), axis=1)
        df['E_score'] = df[e_items].apply(lambda x: normalize(x).mean(), axis=1)
        df['traction'] = df['V_score'] * df['A_score'] * df['E_score']
        
        # Aggregate by segment
        summary = df.groupby(seg_col).agg(
            n=('traction','count'),
            V_mean=('V_score','mean'),
            A_mean=('A_score','mean'),
            E_mean=('E_score','mean'),
            traction_mean=('traction','mean'),
            traction_std=('traction','std')
        ).reset_index()
        summary['Moore'] = summary[seg_col].map(moore_map)
        summary['%'] = (summary['n'] / len(df) * 100).round(1)
        
        print("📊 Traction Diagnosis by Segment\n")
        display(summary[['seg_col','Moore','n','%','V_mean','A_mean','E_mean','traction_mean']].round(3))
        
        # --- PLOT ---
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot A: V|A|E bars
        ax = axes[0]
        x = np.arange(len(summary))
        w = 0.25
        ax.bar(x-w, summary['V_mean'], w, label='VALUE', color='#2c7a7b', edgecolor='black')
        ax.bar(x,   summary['A_mean'], w, label='ACCESS', color='#d69e2e', edgecolor='black')
        ax.bar(x+w, summary['E_mean'], w, label='EVIDENCE', color='#e53e3e', edgecolor='black')
        ax.set_xticks(x); ax.set_xticklabels(summary[seg_col], rotation=15, ha='right')
        ax.set_ylabel('Score (0-1)'); ax.set_title('V | A | E by Segment'); ax.legend(); ax.set_ylim(0,1.05)
        
        # Plot B: Traction Landscape
        ax = axes[1]
        for seg in summary[seg_col]:
            mask = df[seg_col] == seg
            ax.scatter(df.loc[mask,'V_score'], df.loc[mask,'E_score'], alpha=0.15, s=10, label=seg)
        for _, r in summary.iterrows():
            ax.scatter(r['V_mean'], r['E_mean'], s=200, c='black', marker='X', zorder=5)
            ax.annotate(r[seg_col], (r['V_mean'], r['E_mean']), xytext=(5,5), fontsize=9, fontweight='bold')
        
        # Traction contours
        mean_a = df['A_score'].mean()
        Vg, Eg = np.meshgrid(np.linspace(0.01,0.99,100), np.linspace(0.01,0.99,100))
        T = Vg * mean_a * Eg
        ax.contour(Vg, Eg, T, levels=[0.05,0.10,0.20], colors='gray', linestyles='--', alpha=0.7)
        ax.contourf(Vg, Eg, T, levels=[0,0.05], colors=['red'], alpha=0.06)
        ax.set_xlabel('VALUE'); ax.set_ylabel('EVIDENCE'); ax.set_title(f'Traction Landscape (A={mean_a:.2f})')
        ax.set_xlim(0,1); ax.set_ylim(0,1)
        
        plt.tight_layout(); plt.show()
        
        # Pioneer Paradox insight
        pioneer = summary[summary['Moore']=='Early Adopters']
        prag = summary[summary['Moore']=='Early Majority']
        if not pioneer.empty and not prag.empty:
            print(f"\n📝 Pioneer Paradox:")
            print(f"   Pioneers: V={pioneer['V_mean'].values[0]:.2f}, Traction={pioneer['traction_mean'].values[0]:.3f}")
            print(f"   Pragmatists: V={prag['V_mean'].values[0]:.2f}, Traction={prag['traction_mean'].values[0]:.3f}")
            print(f"   → High Value alone doesn't cross the chasm. A and E collapse for Pragmatists.")

btn_run.on_click(compute)

display(widgets.VBox([
    widgets.HTML("<h2>Step 3: Traction Diagnosis (V × A × E)</h2>"),
    widgets.HTML("<p>Map survey items to the 3 pillars. Then compute traction.</p>"),
    widgets.HBox([sel_v, sel_a, sel_e]),
    btn_run,
    out
]))
