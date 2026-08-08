# ═══════════════════════════════════════════════════════════════════
#  STEP 1: Upload & Profile
# ═══════════════════════════════════════════════════════════════════

import io
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output

# --- Upload widgets ---
upload_metric = widgets.FileUpload(
    accept='.csv', multiple=False, description='📁 Metric Conjoint',
    button_style='primary', layout=widgets.Layout(width='300px'))

upload_cbc = widgets.FileUpload(
    accept='.csv', multiple=False, description='📁 CBC',
    button_style='primary', layout=widgets.Layout(width='300px'))

upload_psych = widgets.FileUpload(
    accept='.csv', multiple=False, description='📁 Psychographic',
    button_style='primary', layout=widgets.Layout(width='300px'))

upload_profiles = widgets.FileUpload(
    accept='.csv', multiple=False, description='📁 Design Profiles',
    button_style='primary', layout=widgets.Layout(width='300px'))

out_status = widgets.Output()
out_preview = widgets.Output()

btn_load = widgets.Button(description='▶ Load & Profile', button_style='success')

# --- State ---
metric_df = None
cbc_df = None
psych_df = None
profiles = None

def on_load(_):
    global metric_df, cbc_df, psych_df, profiles
    
    with out_status:
        clear_output()
        
        # Check all files uploaded
        if not upload_metric.value:
            print("❌ Upload metric conjoint CSV first."); return
        if not upload_cbc.value:
            print("❌ Upload CBC CSV first."); return
        if not upload_psych.value:
            print("❌ Upload psychographic CSV first."); return
        if not upload_profiles.value:
            print("❌ Upload design profiles CSV first."); return
        
        # Extract bytes and load
        metric_bytes = list(upload_metric.value.values())[0]['content']
        cbc_bytes = list(upload_cbc.value.values())[0]['content']
        psych_bytes = list(upload_psych.value.values())[0]['content']
        prof_bytes = list(upload_profiles.value.values())[0]['content']
        
        metric_df = pd.read_csv(io.BytesIO(metric_bytes))
        cbc_df = pd.read_csv(io.BytesIO(cbc_bytes))
        psych_df = pd.read_csv(io.BytesIO(psych_bytes))
        profiles = pd.read_csv(io.BytesIO(prof_bytes))
        
        print(f"✅ Metric conjoint: {len(metric_df)} rows ({metric_df['RespID'].nunique()} resp × {metric_df['ProfileID'].nunique()} profiles)")
        print(f"✅ CBC: {len(cbc_df)} rows ({cbc_df['RespID'].nunique()} resp × {cbc_df['Task'].nunique()} tasks)")
        print(f"✅ Psychographic: {len(psych_df)} rows")
        print(f"✅ Design profiles: {len(profiles)} profiles")
        
        # Store in globals for next steps
        import builtins
        builtins.metric_df = metric_df
        builtins.cbc_df = cbc_df
        builtins.psych_df = psych_df
        builtins.profiles = profiles
        
        print("\n✅ All data loaded into namespace. Run Step 2 next.")
    
    with out_preview:
        clear_output()
        print("--- Metric Conjoint Sample ---")
        display(metric_df.head(6))
        print("\n--- CBC Sample (RespID=1, Task=1) ---")
        display(cbc_df[(cbc_df['RespID']==1) & (cbc_df['Task']==1)])
        print("\n--- Psychographic Sample ---")
        display(psych_df.head())
        print("\n--- Rating Distribution ---")
        print(metric_df['Rating'].value_counts().sort_index())
        print("\n--- None Choice Rate ---")
        none_rate = cbc_df[(cbc_df['AltID'] == 4) & (cbc_df['Chosen'] == 1)].shape[0] / (cbc_df['RespID'].nunique() * cbc_df['Task'].nunique())
        print(f"Overall: {none_rate:.1%}")

btn_load.on_click(on_load)

ui = widgets.VBox([
    widgets.HTML("<h2>Step 1: Upload Yana Data Files</h2>"),
    widgets.HTML("<p>Upload all four CSV files, then click Load & Profile.</p>"),
    widgets.HBox([upload_metric, upload_cbc]),
    widgets.HBox([upload_psych, upload_profiles]),
    btn_load,
    out_status,
    out_preview
])

display(ui)
