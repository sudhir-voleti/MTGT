# -*- coding: utf-8 -*-
"""
Lec09 — Step 2: Upload & Inspect the Metric Conjoint Data
Generic tool: upload any metric conjoint CSV with columns [RespID, ProfileID, attribute_cols..., Rating]
Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/02_upload.py').text)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

# =============================================================================
# 1. File Upload Widget for Metric Conjoint Data
# =============================================================================

print("="*60)
print("UPLOAD: Metric Conjoint CSV")
print("="*60)
print("Upload your metric conjoint file (e.g., yana_metric_conjoint_n400.csv)")
print("Required columns: RespID, ProfileID, [attribute columns], Rating")
print("(Optional: Segment column for validation)")
print()

upload_widget = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='Upload CSV',
    layout=widgets.Layout(width='200px')
)

def on_upload_change(change):
    if upload_widget.value:
        # New ipywidgets API: value is a dict of {filename: file_info}
        file_info = list(upload_widget.value.values())[0]
        content = file_info['content']

        # Save to temp path
        temp_path = '/tmp/metric_conjoint_uploaded.csv'
        with open(temp_path, 'wb') as f:
            f.write(content)

        # Load and inspect
        metric_df = pd.read_csv(temp_path)

        clear_output(wait=True)
        print("="*60)
        print("DATA INSPECTION REPORT")
        print("="*60)

        print(f"\n📊 Shape: {metric_df.shape[0]} rows × {metric_df.shape[1]} columns")

        # Detect key columns
        has_resp = 'RespID' in metric_df.columns
        has_profile = 'ProfileID' in metric_df.columns
        has_rating = 'Rating' in metric_df.columns
        has_segment = 'Segment' in metric_df.columns

        if has_resp:
            n_resp = metric_df['RespID'].nunique()
            profiles_per = metric_df.groupby('RespID').size()
            print(f"👥 Respondents: {n_resp}")
            print(f"   Profiles per respondent: {profiles_per.min()}-{profiles_per.max()} (mode: {profiles_per.mode().iloc[0]})")

        print(f"\n📋 Columns: {list(metric_df.columns)}")

        print("\n--- First 5 rows ---")
        display(metric_df.head())

        if has_segment:
            print("\n--- Segment Distribution ---")
            seg_counts = metric_df['Segment'].value_counts()
            print(seg_counts)

        print("\n--- Rating Distribution ---")
        rating_dist = metric_df['Rating'].value_counts().sort_index()
        print(rating_dist)

        # Missing values
        na_counts = metric_df.isna().sum()
        if na_counts.sum() > 0:
            print(f"\n⚠️ Missing values:")
            print(na_counts[na_counts > 0])
        else:
            print(f"\n✓ No missing values")

        # Flat raters check
        if has_resp:
            flat_raters = metric_df.groupby('RespID')['Rating'].nunique()
            n_flat = (flat_raters == 1).sum()
            if n_flat > 0:
                print(f"\n⚠️ {n_flat} respondent(s) gave identical ratings to all profiles")
            else:
                print(f"\n✓ No flat raters detected")

        # Store in global
        globals()['metric_df'] = metric_df

        # Mean rating by profile
        if has_profile and has_rating:
            print("\n" + "="*60)
            print("MEAN RATING BY PROFILE")
            print("="*60)
            profile_means = metric_df.groupby('ProfileID')['Rating'].agg(['mean','std','count']).round(2)
            profile_means = profile_means.reset_index()
            display(profile_means)

            # Bar chart
            fig, ax = plt.subplots(figsize=(10, 5))
            profile_means_sorted = profile_means.sort_values('mean', ascending=True)
            max_mean = profile_means_sorted['mean'].max()
            colors = ['#E37222' if m == max_mean else '#003366' for m in profile_means_sorted['mean']]
            bars = ax.barh(profile_means_sorted['ProfileID'].astype(str), 
                           profile_means_sorted['mean'], color=colors, edgecolor='white')
            ax.set_xlabel('Mean Rating', fontsize=12)
            ax.set_ylabel('Profile ID', fontsize=12)
            ax.set_title('Mean Rating by Profile (highest in orange)', fontsize=13, color='#003366')
            ax.set_xlim(0, metric_df['Rating'].max() + 0.5)
            for bar, mean_val in zip(bars, profile_means_sorted['mean']):
                ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                        f'{mean_val:.2f}', va='center', fontsize=10)
            plt.tight_layout()
            plt.show()

            highest_profile = int(profile_means.loc[profile_means['mean'].idxmax(), 'ProfileID'])
            highest_mean = profile_means['mean'].max()
            print(f"\n🏆 Highest-rated profile: #{highest_profile} (mean = {highest_mean:.2f})")

        # Pause box with reflection
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
            <h3>Pause and Reflect</h3>
            <p>Look at the profile ratings above. Before running any model, answer:</p>
            <table class="scribble-table">
              <thead>
                <tr><th>Question</th><th>My Answer</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td>Which ProfileID has the highest mean rating? Why do you think so?</td>
                  <td><textarea placeholder="Your guess and reasoning..."></textarea></td>
                </tr>
                <tr>
                  <td>Which attribute level appears most often in the top 5 profiles?</td>
                  <td><textarea placeholder="e.g., 150km range, Advanced smart, etc."></textarea></td>
                </tr>
                <tr>
                  <td>Do you see any profiles that are surprisingly low-rated?</td>
                  <td><textarea placeholder="Any surprises in the data?"></textarea></td>
                </tr>
              </tbody>
            </table>
            <p style="margin-top:12px;"><strong>Next:</strong> Run the individual-level analysis to discover which attributes <em>actually</em> drove these ratings.</p>
          </div>
        </div>
        """))

upload_widget.observe(on_upload_change, names='value')
display(upload_widget)
