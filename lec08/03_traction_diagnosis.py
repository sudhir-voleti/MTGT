# ═══════════════════════════════════════════════════════════════════
#  STEP 3: Traction Diagnosis (V × A × E)  —  Redesigned
# ═══════════════════════════════════════════════════════════════════

import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import numpy as np

# ── State guard ──
if 'df' not in globals() or 'seg_col' not in globals() or 'moore_map' not in globals():
    raise RuntimeError("Run Chunks 1 & 2 first! (df, seg_col, moore_map must exist)")

# ── Smart defaults ──
default_v = [c for c in item_cols if any(k in c.lower() for k in ['pioneer','drive','data.hunger','risk.tol','social'])]
default_a = [c for c in item_cols if any(k in c.lower() for k in ['integration','simplicity','support'])]
default_e = [c for c in item_cols if any(k in c.lower() for k in ['compliance','clinical','privacy','accuracy','stigma'])]

# ── Three pillar selectors ──
sel_v = widgets.SelectMultiple(
    description='VALUE', options=item_cols, rows=8,
    value=tuple(default_v),
    layout=widgets.Layout(width='260px', height='220px'))
sel_a = widgets.SelectMultiple(
    description='ACCESS', options=item_cols, rows=8,
    value=tuple(default_a),
    layout=widgets.Layout(width='260px', height='220px'))
sel_e = widgets.SelectMultiple(
    description='EVIDENCE', options=item_cols, rows=8,
    value=tuple(default_e),
    layout=widgets.Layout(width='260px', height='220px'))

# ── Buttons ──
btn_auto   = widgets.Button(description='💡 Auto-Map', button_style='info')
btn_compute= widgets.Button(description='▶ Compute Traction', button_style='primary')
btn_clear  = widgets.Button(description='🗑 Clear', button_style='warning')

# ── Live status area ──
status_html = widgets.HTML("<p><i>Waiting for selections…</i></p>")
out_summary = widgets.Output()
out_results = widgets.Output()

# ── Student exercise: Propose new survey items ──
txt_new_item = widgets.Text(placeholder='E.g., "I need a 30-day money-back guarantee"', 
                            layout=widgets.Layout(width='400px'))
dd_new_pillar = widgets.Dropdown(options=['VALUE','ACCESS','EVIDENCE'], description='Pillar:')
btn_add_item = widgets.Button(description='➕ Add', button_style='info')
proposed_box = widgets.VBox([], layout=widgets.Layout(margin='5px 0'))

# ── Layout ──
selectors = widgets.HBox([
    widgets.VBox([widgets.HTML("<b style='color:#2c7a7b'>📦 VALUE</b><br><span style='font-size:11px'>What they want</span>"), sel_v]),
    widgets.VBox([widgets.HTML("<b style='color:#d69e2e'>🔓 ACCESS</b><br><span style='font-size:11px'>How easy to get</span>"), sel_a]),
    widgets.VBox([widgets.HTML("<b style='color:#e53e3e'>🛡 EVIDENCE</b><br><span style='font-size:11px'>Proof & trust</span>"), sel_e]),
], layout=widgets.Layout(margin='10px 0'))

controls = widgets.HBox([btn_auto, btn_compute, btn_clear])

exercise_ui = widgets.VBox([
    widgets.HTML("<h4>🎓 Exercise: Design Better Survey Items</h4>"),
    widgets.HTML("<p>Current items may not perfectly capture V, A, or E. Propose a new statement and assign it.</p>"),
    widgets.HBox([txt_new_item, dd_new_pillar, btn_add_item]),
    proposed_box
])

ui = widgets.VBox([
    widgets.HTML("<h2>Step 3: Traction Diagnosis</h2>"),
    widgets.HTML("<p><b>Formula:</b> <code>Traction = V × A × E</code> &nbsp;|&nbsp; Each pillar = mean of selected items (0–1 scale).</p>"),
    selectors,
    widgets.HTML("<hr>"),
    controls,
    widgets.VBox([widgets.HTML("<h4>Selection Status</h4>"), status_html, out_summary]),
    widgets.HTML("<hr>"),
    exercise_ui,
    widgets.HTML("<hr>"),
    out_results
])

# ── Helpers ──
def update_status():
    v_set = set(sel_v.value); a_set = set(sel_a.value); e_set = set(sel_e.value)
    overlap = (v_set & a_set) | (v_set & e_set) | (a_set & e_set)
    unused  = set(item_cols) - v_set - a_set - e_set
    
    html = "<ul>"
    html += f"<li><b style='color:#2c7a7b'>VALUE:</b>   {len(v_set)} items</li>"
    html += f"<li><b style='color:#d69e2e'>ACCESS:</b>  {len(a_set)} items</li>"
    html += f"<li><b style='color:#e53e3e'>EVIDENCE:</b> {len(e_set)} items</li>"
    html += f"<li><b>Unused:</b> {len(unused)} items — {list(unused) if unused else 'none'}</li>"
    if overlap:
        html += f"<li style='color:#c53030'><b>⚠️ OVERLAP:</b> {', '.join(overlap)} in multiple pillars!</li>"
    else:
        html += f"<li style='color:#2c7a7b'><b>✅ Clean mapping</b> — no overlaps</li>"
    html += "</ul>"
    status_html.value = html
    
    with out_summary:
        clear_output()
        print("VALUE:  ", list(v_set) or "(none)")
        print("ACCESS: ", list(a_set) or "(none)")
        print("EVIDENCE:", list(e_set) or "(none)")

def on_auto(_):
    sel_v.value = tuple(default_v); sel_a.value = tuple(default_a); sel_e.value = tuple(default_e)
    update_status()

def on_clear(_):
    sel_v.value = (); sel_a.value = (); sel_e.value = ()
    update_status()

def on_compute(_):
    with out_results:
        clear_output()
        v_items = list(sel_v.value); a_items = list(sel_a.value); e_items = list(sel_e.value)
        
        if not (v_items and a_items and e_items):
            print("❌ Select at least one item per pillar."); return
        
        # Warn on overlap but still compute (teaching moment)
        overlap = set(v_items)&set(a_items) | set(v_items)&set(e_items) | set(a_items)&set(e_items)
        if overlap:
            print(f"⚠️  OVERLAP WARNING: {overlap} appear in multiple pillars.\n")
        
        # ── Compute ──
        df['V_score'] = df[v_items].apply(lambda x: normalize(x).mean(), axis=1)
        df['A_score'] = df[a_items].apply(lambda x: normalize(x).mean(), axis=1)
        df['E_score'] = df[e_items].apply(lambda x: normalize(x).mean(), axis=1)
        df['traction'] = df['V_score'] * df['A_score'] * df['E_score']
        
        # ── Aggregate ──
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
        
        # ── Table ──
        print("═"*70)
        print("TRACTION DIAGNOSIS BY SEGMENT")
        print("═"*70)
        display(summary[[seg_col, 'Moore', 'n', '%', 'V_mean', 'A_mean', 'E_mean', 'traction_mean']].round(3))
        print("═"*70)
        
        # ── Plots ──
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
        
        # Plot A: V|A|E bars
        ax = axes[0]
        x = np.arange(len(summary)); w = 0.25
        ax.bar(x-w, summary['V_mean'], w, label='VALUE',   color='#2c7a7b', edgecolor='black')
        ax.bar(x,   summary['A_mean'], w, label='ACCESS',  color='#d69e2e', edgecolor='black')
        ax.bar(x+w, summary['E_mean'], w, label='EVIDENCE',color='#e53e3e', edgecolor='black')
        ax.set_xticks(x); ax.set_xticklabels(summary[seg_col], rotation=15, ha='right')
        ax.set_ylabel('Mean Score (0–1)'); ax.set_title('V | A | E by Segment')
        ax.legend(); ax.set_ylim(0, 1.05)
        
        # Plot B: Traction Landscape
        ax = axes[1]
        for seg in summary[seg_col].unique():
            mask = df[seg_col] == seg
            ax.scatter(df.loc[mask,'V_score'], df.loc[mask,'E_score'], alpha=0.15, s=15, label=seg)
        for _, r in summary.iterrows():
            ax.scatter(r['V_mean'], r['E_mean'], s=200, c='black', marker='X', zorder=5)
            ax.annotate(r[seg_col], (r['V_mean'], r['E_mean']), 
                       textcoords='offset points', xytext=(5,5), fontsize=9, fontweight='bold')
        
        mean_a = df['A_score'].mean()
        Vg, Eg = np.meshgrid(np.linspace(0.01,0.99,100), np.linspace(0.01,0.99,100))
        T = Vg * mean_a * Eg
        ax.contour(Vg, Eg, T, levels=[0.05,0.10,0.20], colors='gray', linestyles='--', alpha=0.7)
        ax.contourf(Vg, Eg, T, levels=[0,0.05], colors=['red'], alpha=0.06)
        ax.set_xlabel('VALUE (V_score)'); ax.set_ylabel('EVIDENCE (E_score)')
        ax.set_title(f'Traction Landscape (A fixed at {mean_a:.2f})')
        ax.set_xlim(0,1); ax.set_ylim(0,1)
        
        plt.tight_layout(); plt.show()
        
        # ── Pioneer Paradox ──
        pioneer = summary[summary['Moore']=='Early Adopters']
        prag    = summary[summary['Moore']=='Early Majority']
        if not pioneer.empty and not prag.empty:
            print(f"\n📝 PIONEER PARADOX:")
            print(f"   Pioneers:    V={pioneer['V_mean'].values[0]:.2f}, Traction={pioneer['traction_mean'].values[0]:.3f}")
            print(f"   Pragmatists: V={prag['V_mean'].values[0]:.2f}, Traction={prag['traction_mean'].values[0]:.3f}")
            print(f"   → High VALUE alone doesn't cross the chasm. A and E collapse for Pragmatists.")

def on_add_item(_):
    if txt_new_item.value.strip():
        lbl = widgets.Label(f"[{dd_new_pillar.value}] {txt_new_item.value.strip()}")
        proposed_box.children += (lbl,)
        txt_new_item.value = ''

# ── Wire ──
sel_v.observe(lambda ch: update_status(), names='value')
sel_a.observe(lambda ch: update_status(), names='value')
sel_e.observe(lambda ch: update_status(), names='value')
btn_auto.on_click(on_auto)
btn_clear.on_click(on_clear)
btn_compute.on_click(on_compute)
btn_add_item.on_click(on_add_item)

update_status()
display(ui)
