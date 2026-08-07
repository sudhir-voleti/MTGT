# ═══════════════════════════════════════════════════════════════════
#  STEP 4: Whole Product Gap Analysis  —  Redesigned
# ═══════════════════════════════════════════════════════════════════

import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import numpy as np

if 'df' not in globals() or 'seg_col' not in globals() or 'moore_map' not in globals():
    raise RuntimeError("Run Chunks 1–3 first!")

# ── Four layer selectors ──
sel_l1  = widgets.SelectMultiple(description='L1 Generic',  options=item_cols, rows=8,
    layout=widgets.Layout(width='240px', height='220px'))
sel_l2  = widgets.SelectMultiple(description='L2 Expected', options=item_cols, rows=8,
    layout=widgets.Layout(width='240px', height='220px'))
sel_l3a = widgets.SelectMultiple(description='L3a Evidence', options=item_cols, rows=8,
    layout=widgets.Layout(width='240px', height='220px'))
sel_l3b = widgets.SelectMultiple(description='L3b Access',   options=item_cols, rows=8,
    layout=widgets.Layout(width='240px', height='220px'))

# Smart defaults
sel_l1.value  = tuple(c for c in item_cols if any(k in c.lower() for k in ['pioneer','drive','data.hunger','risk.tol','social']))
sel_l2.value  = tuple(c for c in item_cols if any(k in c.lower() for k in ['privacy','accuracy','stigma']))
sel_l3a.value = tuple(c for c in item_cols if any(k in c.lower() for k in ['compliance','clinical']))
sel_l3b.value = tuple(c for c in item_cols if any(k in c.lower() for k in ['integration','simplicity','support']))

# ── Buttons ──
btn_auto = widgets.Button(description='💡 Auto-Map', button_style='info')
btn_lock = widgets.Button(description='🔒 Compute Gap', button_style='success')
btn_clear= widgets.Button(description='🗑 Clear', button_style='warning')

# ── Status ──
status_html = widgets.HTML("<p><i>Map items to Whole Product layers...</i></p>")
out_summary = widgets.Output()
out_results = widgets.Output()

# ── Layout ──
selectors = widgets.HBox([
    widgets.VBox([widgets.HTML("<b style='color:#2c7a7b'>📦 L1 Generic</b><br><span style='font-size:11px'>Core innovation</span>"), sel_l1]),
    widgets.VBox([widgets.HTML("<b style='color:#718096'>🛡 L2 Expected</b><br><span style='font-size:11px'>Trust & safety</span>"), sel_l2]),
    widgets.VBox([widgets.HTML("<b style='color:#d69e2e'>📜 L3a Evidence</b><br><span style='font-size:11px'>Proof & standards</span>"), sel_l3a]),
    widgets.VBox([widgets.HTML("<b style='color:#e53e3e'>🔌 L3b Access</b><br><span style='font-size:11px'>Fit & ease</span>"), sel_l3b]),
])

controls = widgets.HBox([btn_auto, btn_lock, btn_clear])

ui = widgets.VBox([
    widgets.HTML("<h2>Step 4: Whole Product Gap Analysis</h2>"),
    widgets.HTML("<p>Moore says you need 4 layers to cross the chasm. Where is Hridayam missing?</p>"),
    selectors,
    widgets.HTML("<hr>"),
    controls,
    widgets.VBox([widgets.HTML("<h4>Layer Status</h4>"), status_html, out_summary]),
    widgets.HTML("<hr>"),
    out_results
])

# ── Helpers ──
def update_status():
    l1=set(sel_l1.value); l2=set(sel_l2.value); l3a=set(sel_l3a.value); l3b=set(sel_l3b.value)
    all_sel = l1|l2|l3a|l3b; unused = set(item_cols)-all_sel
    overlap = (l1&l2)|(l1&l3a)|(l1&l3b)|(l2&l3a)|(l2&l3b)|(l3a&l3b)
    
    html = "<ul>"
    html += f"<li><b style='color:#2c7a7b'>L1 Generic:</b>  {len(l1)} items</li>"
    html += f"<li><b style='color:#718096'>L2 Expected:</b> {len(l2)} items</li>"
    html += f"<li><b style='color:#d69e2e'>L3a Evidence:</b> {len(l3a)} items</li>"
    html += f"<li><b style='color:#e53e3e'>L3b Access:</b>   {len(l3b)} items</li>"
    html += f"<li><b>Unused:</b> {len(unused)} items</li>"
    if overlap:
        html += f"<li style='color:#c53030'><b>⚠️ OVERLAP:</b> {', '.join(overlap)}</li>"
    else:
        html += f"<li style='color:#2c7a7b'><b>✅ Clean mapping</b></li>"
    html += "</ul>"
    status_html.value = html
    
    with out_summary:
        clear_output()
        print("L1: ", list(l1) or "(none)")
        print("L2: ", list(l2) or "(none)")
        print("L3a:", list(l3a) or "(none)")
        print("L3b:", list(l3b) or "(none)")

def on_auto(_):
    sel_l1.value  = tuple(c for c in item_cols if any(k in c.lower() for k in ['pioneer','drive','data.hunger','risk.tol','social']))
    sel_l2.value  = tuple(c for c in item_cols if any(k in c.lower() for k in ['privacy','accuracy','stigma']))
    sel_l3a.value = tuple(c for c in item_cols if any(k in c.lower() for k in ['compliance','clinical']))
    sel_l3b.value = tuple(c for c in item_cols if any(k in c.lower() for k in ['integration','simplicity','support']))
    update_status()

def on_clear(_):
    sel_l1.value=(); sel_l2.value=(); sel_l3a.value=(); sel_l3b.value=()
    update_status()

def on_lock(_):
    global wp_map
    with out_results:
        clear_output()
        l1=list(sel_l1.value); l2=list(sel_l2.value); l3a=list(sel_l3a.value); l3b=list(sel_l3b.value)
        wp_map = {'L1_Generic':l1, 'L2_Expected':l2, 'L3a_Evidence':l3a, 'L3b_Access':l3b}
        
        for name, cols in wp_map.items():
            df[f'{name}_score'] = df[cols].apply(lambda x: normalize(x).mean(), axis=1) if cols else 0.0
        
        levels = ['L1_Generic_score','L2_Expected_score','L3a_Evidence_score','L3b_Access_score']
        level_names = ['L1','L2','L3a','L3b']
        
        # Segment summary — BUG FIX: use seg_col variable, not string 'seg_col'
        seg = df.groupby(seg_col)[levels].mean().reset_index()
        seg['Moore'] = seg[seg_col].map(moore_map)
        counts = df[seg_col].value_counts()
        seg['n'] = seg[seg_col].map(counts)
        seg['%'] = (seg['n']/len(df)*100).round(1)
        
        # Gap detection
        def find_gap(row):
            highest = -1
            for i, lv in enumerate(levels):
                if row[lv] >= 0.50: highest = i
            if highest == -1: return "No Core Demand"
            if highest == len(levels)-1: return "None — Ready"
            nxt = levels[highest+1]
            return f"{level_names[highest+1]} Gap" if row[nxt] < 0.40 else "None"
        seg['Gap'] = seg.apply(find_gap, axis=1)
        
        # ── Display ──
        print("═"*70)
        print("WHOLE PRODUCT LAYER SCORES & GAPS")
        print("═"*70)
        disp_cols = [seg_col, 'Moore'] + levels + ['Gap', 'n', '%']
        print(seg[disp_cols].round(3).to_string(index=False))
        print("═"*70)
        
        # ── Plots ──
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
        
        # Plot A: Layer profiles
        ax = axes[0]
        x = np.arange(len(seg)); w = 0.2
        colors = ['#2c7a7b','#718096','#d69e2e','#e53e3e']
        for i, (lv, name) in enumerate(zip(levels, level_names)):
            ax.bar(x + i*w, seg[lv], w, label=name, color=colors[i], edgecolor='black', linewidth=0.5)
        ax.axhline(0.50, color='red', linestyle='--', alpha=0.6, label='Threshold')
        ax.set_xticks(x + 1.5*w); ax.set_xticklabels(seg[seg_col], rotation=15, ha='right')
        ax.set_ylabel('Mean Score (0–1)'); ax.set_title('Whole Product Demand by Segment')
        ax.legend(loc='upper right'); ax.set_ylim(0, 1.05)
        
        # Plot B: Chasm Readiness
        ax = axes[1]
        for _, r in seg.iterrows():
            x_val = r['L1_Generic_score']
            y_val = (r['L3a_Evidence_score'] + r['L3b_Access_score'])/2
            ax.scatter(x_val, y_val, s=r['n']*5, alpha=0.7, edgecolors='black', linewidth=1.5)
            ax.annotate(r[seg_col], (x_val, y_val), textcoords='offset points', 
                       xytext=(5,5), fontsize=9, fontweight='bold')
        ax.axvline(0.50, color='gray', linestyle='--', alpha=0.5)
        ax.axhline(0.50, color='gray', linestyle='--', alpha=0.5)
        ax.text(0.25, 0.75, 'Chasm\n(High Demand,\nLow Supply)', ha='center', va='center',
               fontsize=10, color='#c53030', fontweight='bold', alpha=0.8)
        ax.text(0.75, 0.75, 'Whole Product\nReady', ha='center', va='center',
               fontsize=10, color='#2c7a7b', fontweight='bold', alpha=0.8)
        ax.text(0.25, 0.25, 'Low\nInterest', ha='center', va='center',
               fontsize=10, color='#718096', fontweight='bold', alpha=0.8)
        ax.text(0.75, 0.25, 'Visionary\nOnly', ha='center', va='center',
               fontsize=10, color='#d69e2e', fontweight='bold', alpha=0.8)
        ax.set_xlabel('L1 Generic Product (Supply)')
        ax.set_ylabel('(L3a Evidence + L3b Access) / 2  (Demand)')
        ax.set_title('Chasm Readiness Map'); ax.set_xlim(0,1); ax.set_ylim(0,1)
        
        plt.tight_layout(); plt.show()

# ── Wire ──
sel_l1.observe(lambda ch: update_status(), names='value')
sel_l2.observe(lambda ch: update_status(), names='value')
sel_l3a.observe(lambda ch: update_status(), names='value')
sel_l3b.observe(lambda ch: update_status(), names='value')
btn_auto.on_click(on_auto)
btn_clear.on_click(on_clear)
btn_lock.on_click(on_lock)

update_status()
display(ui)
