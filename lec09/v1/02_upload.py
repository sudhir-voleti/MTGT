# -*- coding: utf-8 -*-
"""
Lec09 — Step 2: Upload & Map Columns (Generic Metric Conjoint Inspector)
Interactive: upload any CSV, then map columns via dropdowns before analysis.
Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/02_upload.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

# Global state
_state = {'df': None, 'mapping': {}}

# =============================================================================
# 1. Upload Widget
# =============================================================================

print("="*60)
print("STEP 1: UPLOAD YOUR METRIC CONJOINT CSV")
print("="*60)
print("Upload any CSV file with respondent ratings and attribute columns.")
print()

upload_widget = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='Upload CSV',
    layout=widgets.Layout(width='200px')
)

def on_upload(change):
    if not upload_widget.value:
        return

    file_info = list(upload_widget.value.values())[0]
    content = file_info['content']

    temp_path = '/tmp/metric_conjoint_uploaded.csv'
    with open(temp_path, 'wb') as f:
        f.write(content)

    df = pd.read_csv(temp_path)
    _state['df'] = df

    clear_output(wait=True)
    print("="*60)
    print("STEP 2: PREVIEW & COLUMN MAPPING")
    print("="*60)

    print(f"\n📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"📋 Available columns: {list(df.columns)}")

    print("\n--- First 5 rows ---")
    display(df.head())

    print("\n--- Column data types ---")
    dtype_df = pd.DataFrame({'Column': df.columns, 'Type': df.dtypes.values, 'Unique': [df[c].nunique() for c in df.columns]})
    display(dtype_df)

    # -------------------------------------------------------------------------
    # Mapping widgets
    # -------------------------------------------------------------------------

    cols = list(df.columns)
    numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]

    # Guess defaults
    default_resp = next((c for c in cols if 'resp' in c.lower() or 'id' in c.lower()), cols[0])
    default_task = next((c for c in cols if 'profile' in c.lower() or 'task' in c.lower()), None)
    default_y = next((c for c in numeric_cols if 'rating' in c.lower() or 'score' in c.lower() or 'choice' in c.lower()), numeric_cols[0] if numeric_cols else cols[0])

    dropdown_resp = widgets.Dropdown(
        options=cols, value=default_resp,
        description='Respondent ID:', layout=widgets.Layout(width='350px'),
        style={'description_width': '120px'}
    )

    task_options = ['(None)'] + cols
    dropdown_task = widgets.Dropdown(
        options=task_options, value=default_task if default_task else '(None)',
        description='Task/Profile ID:', layout=widgets.Layout(width='350px'),
        style={'description_width': '120px'}
    )

    dropdown_y = widgets.Dropdown(
        options=cols, value=default_y,
        description='Rating (Y):', layout=widgets.Layout(width='350px'),
        style={'description_width': '120px'}
    )

    # Attribute columns: exclude the ones already selected for ID/Y
    attr_select = widgets.SelectMultiple(
        options=cols,
        value=tuple([c for c in cols if c not in [default_resp, default_task, default_y]]),
        description='Attributes (X):',
        layout=widgets.Layout(width='350px', height='150px'),
        style={'description_width': '120px'}
    )

    # Update attr_select when resp/task/y change
    def update_attrs(*args):
        reserved = {dropdown_resp.value, dropdown_y.value}
        if dropdown_task.value != '(None)':
            reserved.add(dropdown_task.value)
        new_options = [c for c in cols if c not in reserved]
        attr_select.options = new_options
        # Keep currently selected if still valid
        new_value = tuple(v for v in attr_select.value if v in new_options)
        if new_value:
            attr_select.value = new_value

    dropdown_resp.observe(update_attrs, names='value')
    dropdown_task.observe(update_attrs, names='value')
    dropdown_y.observe(update_attrs, names='value')

    confirm_btn = widgets.Button(
        description='✓ Confirm & Analyze',
        button_style='success',
        layout=widgets.Layout(width='200px', margin='10px 0')
    )

    def on_confirm(b):
        _state['mapping'] = {
            'resp_id': dropdown_resp.value,
            'task_id': dropdown_task.value if dropdown_task.value != '(None)' else None,
            'y_col': dropdown_y.value,
            'attr_cols': list(attr_select.value)
        }
        run_analysis()

    confirm_btn.on_click(on_confirm)

    print("\n👉 Map your columns below, then click 'Confirm & Analyze':")
    display(widgets.VBox([
        dropdown_resp,
        dropdown_task,
        dropdown_y,
        attr_select,
        confirm_btn
    ]))

upload_widget.observe(on_upload, names='value')
display(upload_widget)

# =============================================================================
# 2. Analysis (runs after mapping is confirmed)
# =============================================================================

def run_analysis():
    df = _state['df']
    m = _state['mapping']

    resp_col = m['resp_id']
    task_col = m['task_id']
    y_col = m['y_col']
    attr_cols = m['attr_cols']

    clear_output(wait=True)
    print("="*60)
    print("DATA INSPECTION REPORT")
    print("="*60)

    print(f"\n📊 Mapped columns:")
    print(f"   Respondent ID : {resp_col}")
    print(f"   Task/Profile  : {task_col if task_col else '(not set)'}")
    print(f"   Rating (Y)    : {y_col}")
    print(f"   Attributes (X): {attr_cols}")

    # Store in globals for next cells
    globals()['metric_df'] = df
    globals()['col_mapping'] = m

    # Respondent count
    n_resp = df[resp_col].nunique()
    tasks_per = df.groupby(resp_col).size()
    print(f"\n👥 Respondents: {n_resp}")
    print(f"   Observations per respondent: {tasks_per.min()}-{tasks_per.max()} (mode: {tasks_per.mode().iloc[0]})")

    # Rating stats
    print(f"\n📈 {y_col} statistics:")
    print(df[y_col].describe().round(2))

    # Missing values
    relevant_cols = [resp_col, y_col] + attr_cols
    na_counts = df[relevant_cols].isna().sum()
    if na_counts.sum() > 0:
        print(f"\n⚠️ Missing values in mapped columns:")
        print(na_counts[na_counts > 0])
    else:
        print(f"\n✓ No missing values in mapped columns")

    # Flat raters
    flat = df.groupby(resp_col)[y_col].nunique()
    n_flat = (flat == 1).sum()
    if n_flat > 0:
        print(f"\n⚠️ {n_flat} respondent(s) gave identical {y_col} to all profiles")
    else:
        print(f"\n✓ No flat raters detected")

    # Attribute level summaries
    print("\n" + "="*60)
    print("ATTRIBUTE LEVEL SUMMARIES")
    print("="*60)
    for col in attr_cols:
        print(f"\n{col}:")
        vc = df[col].value_counts().sort_index()
        print(f"  {dict(vc)}")

    # Mean rating by task/profile if available
    if task_col:
        print("\n" + "="*60)
        print(f"MEAN {y_col.upper()} BY {task_col.upper()}")
        print("="*60)
        profile_means = df.groupby(task_col)[y_col].agg(['mean','std','count']).round(2)
        profile_means = profile_means.reset_index()
        display(profile_means)

        # Bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        pm_sorted = profile_means.sort_values('mean', ascending=True)
        max_mean = pm_sorted['mean'].max()
        colors = ['#E37222' if m == max_mean else '#003366' for m in pm_sorted['mean']]
        bars = ax.barh(pm_sorted[task_col].astype(str), pm_sorted['mean'], color=colors, edgecolor='white')
        ax.set_xlabel(f'Mean {y_col}', fontsize=12)
        ax.set_ylabel(task_col, fontsize=12)
        ax.set_title(f'Mean {y_col} by {task_col} (highest in orange)', fontsize=13, color='#003366')
        ax.set_xlim(0, df[y_col].max() + 0.5)
        for bar, mean_val in zip(bars, pm_sorted['mean']):
            ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, 
                    f'{mean_val:.2f}', va='center', fontsize=10)
        plt.tight_layout()
        plt.show()

        highest = int(pm_sorted.iloc[-1][task_col])
        print(f"\n🏆 Highest-rated {task_col}: #{highest} (mean = {max_mean:.2f})")

    # Segment check
    has_segment = 'Segment' in df.columns
    if has_segment:
        print("\n" + "="*60)
        print("SEGMENT DISTRIBUTION")
        print("="*60)
        print(df['Segment'].value_counts())

    # Scribble pause
    display(HTML("""
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
        <h3>Pause and Reflect: Before You Model</h3>
        <p>You have mapped the columns and inspected the data. Now commit your intuition:</p>
        <table class="scribble-table">
          <thead>
            <tr><th>Question</th><th>My Answer</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>Which attribute do you think will have the biggest impact on the rating?</td>
              <td><textarea placeholder="e.g., Price, because..."></textarea></td>
            </tr>
            <tr>
              <td>Which attribute level do you expect to have the highest part-worth?</td>
              <td><textarea placeholder="e.g., 150km range, because..."></textarea></td>
            </tr>
            <tr>
              <td>Do you think respondents are homogeneous, or will there be distinct segments?</td>
              <td><textarea placeholder="e.g., 2-3 segments based on..."></textarea></td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top:12px;"><strong>Next:</strong> Run the individual-level OLS cell to estimate part-worths and test your predictions.</p>
      </div>
    </div>
    """))
