"""Chunk 2: Name your segments and map them to Moore's categories."""
from IPython.display import HTML

if 'df' not in globals():
    raise RuntimeError("Run Chunk 1 first!")

# --- Build mapping UI ---
moore_opts = ['-- Pick One --', 'Innovators', 'Early Adopters', 
              'Early Majority', 'Late Majority', 'Laggards']

seg_names = sorted(df[seg_col].dropna().unique().astype(str))
rows = []
moore_drops = {}

for s in seg_names:
    lbl = widgets.Label(s, layout=widgets.Layout(width='150px'))
    dd = widgets.Dropdown(options=moore_opts, value='-- Pick One --',
                          layout=widgets.Layout(width='180px'))
    moore_drops[s] = dd
    rows.append(widgets.HBox([lbl, dd]))

# --- Auto-suggest heuristics ---
def auto_suggest(_):
    for s, dd in moore_drops.items():
        low = s.lower()
        if any(k in low for k in ['pioneer','vision','early']): dd.value = 'Early Adopters'
        elif any(k in low for k in ['pragmat','majority']): dd.value = 'Early Majority'
        elif any(k in low for k in ['skept','risk','late']): dd.value = 'Late Majority'
        elif any(k in low for k in ['disengage','lag','none']): dd.value = 'Laggards'

btn_auto = widgets.Button(description='💡 Auto-Suggest', button_style='info')
btn_auto.on_click(auto_suggest)

btn_lock = widgets.Button(description='🔒 Lock Mapping', button_style='success')
out_lock = widgets.Output()

def lock_mapping(_):
    global moore_map
    unmapped = [s for s, dd in moore_drops.items() if dd.value == '-- Pick One --']
    if unmapped:
        with out_lock: 
            clear_output()
            print(f"❌ Please map these first: {', '.join(unmapped)}")
        return
    
    moore_map = {s: dd.value for s, dd in moore_drops.items()}
    with out_lock:
        clear_output()
        print("✅ Moore Mapping Locked!\n")
        for s, m in moore_map.items():
            n = (df[seg_col] == s).sum()
            print(f"  {s:12s} → {m:18s} (n={n})")
        print("\n🚀 You can now run Chunk 3 (Traction).")

btn_lock.on_click(lock_mapping)

display(widgets.VBox([
    widgets.HTML("<h2>Step 2: Map Segments to Moore Categories</h2>"),
    widgets.HTML("<p>Geoffrey Moore says markets have 5 types of buyers. Which is which?</p>"),
    widgets.VBox(rows),
    widgets.HBox([btn_auto, btn_lock]),
    out_lock
]))
