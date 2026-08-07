"""Chunk 1: Upload your survey data and meet your segments."""
import io

# --- Upload widget ---
upload = widgets.FileUpload(accept='.csv', multiple=False, description='📁 Upload CSV')
out = widgets.Output()

def on_upload(change):
    global df, item_cols, seg_col
    if not upload.value:
        return
    raw = list(upload.value.values())[0]['content']
    df = pd.read_csv(io.BytesIO(raw))
    
    # Auto-detect segment column
    candidates = [c for c in df.columns if 'segment' in c.lower() or 'membership' in c.lower()]
    seg_col = candidates[0] if candidates else df.columns[0]
    
    # Detect numeric survey items (exclude segment)
    item_cols = [c for c in df.columns 
                 if c != seg_col 
                 and pd.api.types.is_numeric_dtype(df[c])]
    
    with out:
        clear_output()
        print(f"✅ Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"🔍 Segment column detected: '{seg_col}'")
        print(f"📊 Numeric survey items found: {len(item_cols)}")
        print("\n--- Segment Sizes ---")
        vc = df[seg_col].value_counts().sort_index()
        for seg, n in vc.items():
            print(f"  {seg}: {n} ({n/len(df)*100:.1f}%)")
        print("\n--- First 5 Rows ---")
        display(df.head())

upload.observe(on_upload, names='value')
display(widgets.VBox([widgets.HTML("<h2>Step 1: Upload Hridayam Survey Data</h2>"), upload, out]))
