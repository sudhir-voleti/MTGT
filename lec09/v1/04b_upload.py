# -*- coding: utf-8 -*-
"""
Lec09 — Step 4b: Upload & Inspect CBC Data (Generic)
Interactive column mapping + sample choice task walkthrough.
Pure code cell. Run AFTER 04a_theory.py in a separate Colab cell.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/04b_upload.py').text)
"""

import pandas as pd
import numpy as np
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

_state = {'df': None, 'mapping': None}

# =============================================================================
# 1. Upload widget
# =============================================================================

print("="*60)
print("STEP 4b: UPLOAD CBC DATA")
print("="*60)
print("Upload your CBC choice file (e.g., yana_cbc_n400.csv)")
print("Format: long format — one row per alternative per choice task")
print()

upload_widget = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='Upload CBC CSV',
    layout=widgets.Layout(width='200px')
)

def on_upload(change):
    if not upload_widget.value:
        return

    file_info = list(upload_widget.value.values())[0]
    content = file_info['content']

    temp_path = '/tmp/cbc_uploaded.csv'
    with open(temp_path, 'wb') as f:
        f.write(content)

    df = pd.read_csv(temp_path)
    _state['df'] = df

    clear_output(wait=True)
    print("="*60)
    print("STEP 4b: COLUMN MAPPING")
    print("="*60)

    print(f"\n📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"📋 Columns: {list(df.columns)}")

    print("\n--- First 8 rows (should show multiple alternatives per task) ---")
    display(df.head(8))

    cols = list(df.columns)

    # Guesses
    def guess(patterns, exclude=None):
        for c in cols:
            if exclude and c in exclude:
                continue
            if any(p in c.lower() for p in patterns):
                return c
        return None

    default_resp = guess(['resp', 'id'], exclude=None) or cols[0]
    default_task = guess(['task', 'set'], exclude={default_resp}) or '(None)'
    default_alt = guess(['alt', 'option', 'choice_id'], exclude={default_resp}) or '(None)'
    default_choice = guess(['chosen', 'choice', 'select'], exclude={default_resp, default_task, default_alt}) or cols[-1]

    dd_resp = widgets.Dropdown(options=cols, value=default_resp, description='Resp ID:', layout=widgets.Layout(width='350px'))
    dd_task = widgets.Dropdown(options=['(None)'] + cols, value=default_task if default_task else '(None)', description='Task ID:', layout=widgets.Layout(width='350px'))
    dd_alt = widgets.Dropdown(options=['(None)'] + cols, value=default_alt if default_alt else '(None)', description='Alt ID:', layout=widgets.Layout(width='350px'))
    dd_choice = widgets.Dropdown(options=cols, value=default_choice, description='Choice:', layout=widgets.Layout(width='350px'))

    reserved = set()
    attr_sel = widgets.SelectMultiple(options=cols, description='Attributes:', layout=widgets.Layout(width='350px', height='150px'))

    def upd(*args):
        rsv = {dd_resp.value, dd_choice.value}
        if dd_task.value != '(None)': rsv.add(dd_task.value)
        if dd_alt.value != '(None)': rsv.add(dd_alt.value)
        attr_sel.options = [c for c in cols if c not in rsv]

    for w in [dd_resp, dd_task, dd_alt, dd_choice]:
        w.observe(upd, names='value')
    upd()

    btn = widgets.Button(description='✓ Confirm & Inspect', button_style='success')
    def on_conf(b):
        _state['mapping'] = {
            'resp_id': dd_resp.value,
            'task_id': dd_task.value if dd_task.value != '(None)' else None,
            'alt_id': dd_alt.value if dd_alt.value != '(None)' else None,
            'choice': dd_choice.value,
            'attr_cols': list(attr_sel.value)
        }
        run_inspection()
    btn.on_click(on_conf)
    display(widgets.VBox([dd_resp, dd_task, dd_alt, dd_choice, attr_sel, btn]))

upload_widget.observe(on_upload, names='value')
display(upload_widget)

# =============================================================================
# 2. Inspection + sample task walkthrough
# =============================================================================

def run_inspection():
    df = _state['df']
    m = _state['mapping']
    resp_col = m['resp_id']
    task_col = m['task_id']
    alt_col = m['alt_id']
    choice_col = m['choice']
    attr_cols = m['attr_cols']

    clear_output(wait=True)
    print("="*60)
    print("CBC DATA INSPECTION")
    print("="*60)

    print(f"\n📊 Mapped columns:")
    print(f"   Respondent ID : {resp_col}")
    print(f"   Task ID       : {task_col if task_col else '(not set)'}")
    print(f"   Alternative ID: {alt_col if alt_col else '(not set)'}")
    print(f"   Choice        : {choice_col}")
    print(f"   Attributes    : {attr_cols}")

    n_resp = df[resp_col].nunique()
    print(f"\n👥 Respondents: {n_resp}")

    if task_col:
        tasks_per = df.groupby(resp_col)[task_col].nunique()
        print(f"   Tasks per respondent: {tasks_per.min()}-{tasks_per.max()} (mode: {tasks_per.mode().iloc[0]})")

    if alt_col:
        alts_per_task = df.groupby([resp_col, task_col] if task_col else resp_col)[alt_col].nunique()
        print(f"   Alternatives per task: {alts_per_task.min()}-{alts_per_task.max()} (mode: {alts_per_task.mode().iloc[0]})")

    # Check choice structure
    choice_check = df.groupby([resp_col, task_col] if task_col else resp_col)[choice_col].sum() if task_col else df.groupby(resp_col)[choice_col].sum()
    bad_tasks = (choice_check != 1).sum()
    if bad_tasks > 0:
        print(f"\n⚠️ {bad_tasks} task(s) do not have exactly 1 chosen alternative")
    else:
        print(f"\n✓ Each task has exactly 1 chosen alternative")

    # Missing values
    relevant = [resp_col, choice_col] + attr_cols
    if task_col: relevant.append(task_col)
    if alt_col: relevant.append(alt_col)
    na_counts = df[relevant].isna().sum()
    if na_counts.sum() > 0:
        print(f"\n⚠️ Missing values:")
        print(na_counts[na_counts > 0])
    else:
        print(f"\n✓ No missing values in mapped columns")

    # -------------------------------------------------------------------------
    # Sample choice task walkthrough
    # -------------------------------------------------------------------------

    print("\n" + "="*60)
    print("SAMPLE CHOICE TASK")
    print("="*60)

    sample_resp = df[resp_col].iloc[0]
    if task_col:
        sample_task = df[df[resp_col] == sample_resp][task_col].iloc[0]
        sample_data = df[(df[resp_col] == sample_resp) & (df[task_col] == sample_task)].copy()
        print(f"\nRespondent {sample_resp}, Task {sample_task}:")
    else:
        sample_data = df[df[resp_col] == sample_resp].head(4).copy()
        print(f"\nRespondent {sample_resp} (first 4 alternatives):")

    display_cols = [resp_col]
    if task_col: display_cols.append(task_col)
    if alt_col: display_cols.append(alt_col)
    display_cols += attr_cols + [choice_col]
    display(sample_data[display_cols])

    chosen_row = sample_data[sample_data[choice_col] == 1]
    if len(chosen_row) > 0:
        chosen_idx = chosen_row.index[0]
        if alt_col:
            chosen_alt = chosen_row[alt_col].values[0]
            print(f"\n→ This respondent chose Alternative {chosen_alt}")
        else:
            print(f"\n→ This respondent chose the row marked with {choice_col}=1")

        # Describe the chosen alternative
        desc_parts = []
        for col in attr_cols:
            val = chosen_row[col].values[0]
            if pd.notna(val) and str(val).lower() not in ['none', 'nan']:
                desc_parts.append(f"{col}={val}")
        if desc_parts:
            print(f"   Configuration: {', '.join(desc_parts)}")

    # Detect None alternative
    if alt_col:
        # Check if highest alt_id is "None"
        max_alt = df[alt_col].max()
        none_rows = df[df[alt_col] == max_alt]
        if len(none_rows) > 0 and attr_cols:
            first_none = none_rows[attr_cols[0]].iloc[0]
            if str(first_none).lower() in ['none', 'nan']:
                print(f"\n✓ Detected 'None' alternative: AltID = {max_alt}")
                none_rate = (df[df[alt_col] == max_alt][choice_col] == 1).mean()
                print(f"   Overall 'None' choice rate: {none_rate:.1%}")

    # Store in globals
    globals()['cbc_df'] = df
    globals()['cbc_mapping'] = m

    # -------------------------------------------------------------------------
    # Scribble pause
    # -------------------------------------------------------------------------

    # Use string concatenation instead of .format() to avoid CSS curly brace conflicts
    html_content = """
    <style>
      .caselet-body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; 
                      font-size: 15px; line-height: 1.55; color: #1e293b; max-width: 860px; margin: 0 auto; }
      .caselet-body h2 { font-size: 1.2em; color: #003366; border-bottom: 2px solid #E37222; 
                         padding-bottom: 4px; margin-top: 28px; }
      .caselet-body .pause-box { background: #fffbeb; border: 1px dashed #d97706; 
                                 padding: 16px 18px; margin: 22px 0; }
      .caselet-body .pause-box h3 { font-size: 1.05em; color: #003366; margin-top: 0; }
      .caselet-body textarea { width: 100%; min-height: 50px; padding: 8px 10px; 
                                border: 1px solid #cbd5e1; border-radius: 6px; 
                                font-family: inherit; font-size: 14px; box-sizing: border-box; resize: vertical; }
      .caselet-body .scribble-table th { background-color: #475569; color: white; 
                                          font-size: 13.5px; padding: 9px 12px; text-align: left; }
      .caselet-body .scribble-table td { padding: 8px 12px; vertical-align: top; border: 1px solid #d0d7de; }
    </style>
    <div class="caselet-body">
      <div class="pause-box">
        <h3>Pause and Reflect: Which Would You Choose?</h3>
        <p>Look at the sample choice task above. If you were Respondent """ + str(sample_resp) + """, which alternative would you pick?</p>
        <table class="scribble-table">
          <thead>
            <tr><th>My Choice (AltID)</th><th>Why I would choose this</th><th>What I would sacrifice</th></tr>
          </thead>
          <tbody>
            <tr>
              <td><textarea placeholder="e.g., Alt 3..."></textarea></td>
              <td><textarea placeholder="Because it has the best price..."></textarea></td>
              <td><textarea placeholder="I give up range and brand..."></textarea></td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top:12px;"><strong>Next:</strong> Run 04c_mnl.py to estimate the choice model and see what the <em>aggregate</em> market actually prefers.</p>
      </div>
    </div>
    """
    display(HTML(html_content))
