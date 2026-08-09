# -*- coding: utf-8 -*-
"""
Lec09 — Step 2: Upload & Inspect the Metric Conjoint Data
Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/02_upload.py').text)
Prerequisite: 01_theory.py should have been run first.
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display, clear_output
import ipywidgets as widgets

# =============================================================================
# 1. Auto-fetch the 16 profiles from GitHub
# =============================================================================

PROFILES_URL = "https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/yana_profiles_16.csv"

try:
    profiles = pd.read_csv(PROFILES_URL)
    print(f"✓ Auto-fetched {len(profiles)} profiles from GitHub")
    print(f"  Columns: {list(profiles.columns)}")
except Exception as e:
    print(f"✗ Could not fetch profiles from GitHub: {e}")
    print("  Please upload yana_profiles_16.csv manually if needed.")
    profiles = None

# =============================================================================
# 2. File Upload Widget for Metric Conjoint Data
# =============================================================================

print("\n" + "="*60)
print("UPLOAD: yana_metric_conjoint_n400.csv")
print("="*60)
print("Please upload the metric conjoint CSV file below.")
print("(Drag and drop or click the Upload button)")

upload_widget = widgets.FileUpload(
    accept='.csv',
    multiple=False,
    description='Upload CSV',
    layout=widgets.Layout(width='200px')
)

def on_upload_change(change):
    if len(upload_widget.value) > 0:
        # Get the uploaded file
        uploaded_file = upload_widget.value[0]
        content = uploaded_file['content']

        # Save to a temporary path
        temp_path = '/tmp/yana_metric_conjoint_n400.csv'
        with open(temp_path, 'wb') as f:
            f.write(content)

        # Load and inspect
        metric_df = pd.read_csv(temp_path)

        clear_output(wait=True)
        print("="*60)
        print("DATA INSPECTION REPORT")
        print("="*60)

        print(f"\n📊 Shape: {metric_df.shape[0]} rows × {metric_df.shape[1]} columns")
        print(f"   Expected: 6,400 rows (400 respondents × 16 profiles)")

        print(f"\n👥 Respondents: {metric_df['RespID'].nunique()}")
        print(f"   Profiles per respondent: {metric_df.groupby('RespID').size().iloc[0]}")

        print(f"\n📋 Columns: {list(metric_df.columns)}")

        print("\n--- First 5 rows ---")
        display(metric_df.head())

        print("\n--- Segment Distribution ---")
        seg_counts = metric_df['Segment'].value_counts()
        print(seg_counts)

        print("\n--- Rating Distribution ---")
        rating_dist = metric_df['Rating'].value_counts().sort_index()
        print(rating_dist)

        # Check for missing values
        na_counts = metric_df.isna().sum()
        if na_counts.sum() > 0:
            print(f"\n⚠️ Missing values detected:")
            print(na_counts[na_counts > 0])
        else:
            print(f"\n✓ No missing values")

        # Check for flat raters (same rating across all 16 profiles)
        flat_raters = metric_df.groupby('RespID')['Rating'].nunique()
        n_flat = (flat_raters == 1).sum()
        if n_flat > 0:
            print(f"\n⚠️ {n_flat} respondent(s) gave the same rating to all 16 profiles")
        else:
            print(f"\n✓ No flat raters detected")

        # Store in global for next cells
        globals()['metric_df'] = metric_df
        globals()['profiles'] = profiles

        # Show the profile descriptions
        if profiles is not None:
            print("\n" + "="*60)
            print("PROFILE REFERENCE TABLE")
            print("="*60)
            display(profiles)

        # Mean rating by profile
        print("\n" + "="*60)
        print("MEAN RATING BY PROFILE")
        print("="*60)
        profile_means = metric_df.groupby('ProfileID')['Rating'].agg(['mean','std','count']).round(2)
        profile_means = profile_means.reset_index()
        if profiles is not None:
            profile_means = profile_means.merge(profiles, on='ProfileID')
        display(profile_means)

        # Bar chart
        fig, ax = plt.subplots(figsize=(12, 5))
        profile_means_sorted = profile_means.sort_values('mean', ascending=True)
        colors = ['#E37222' if m == profile_means_sorted['mean'].max() else '#003366' 
                  for m in profile_means_sorted['mean']]
        bars = ax.barh(profile_means_sorted['ProfileID'].astype(str), 
                       profile_means_sorted['mean'], color=colors, edgecolor='white')
        ax.set_xlabel('Mean Rating (1–10)', fontsize=12)
        ax.set_ylabel('Profile ID', fontsize=12)
        ax.set_title('Mean Rating by Profile (highest in orange)', fontsize=13, color='#003366')
        ax.set_xlim(0, 10)
        for bar, mean_val in zip(bars, profile_means_sorted['mean']):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    f'{mean_val:.2f}', va='center', fontsize=10)
        plt.tight_layout()
        plt.show()

        # Store highest profile info
        highest_profile = profile_means.loc[profile_means['mean'].idxmax(), 'ProfileID']
        highest_mean = profile_means['mean'].max()
        print(f"\n🏆 Highest-rated profile: #{int(highest_profile)} (mean = {highest_mean:.2f})")

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
            <h3>Pause and Reflect: How Did Your Prediction Do?</h3>
            <p>Look back at your Prediction 1 from the theory section. Did you guess the highest-rated profile correctly?</p>
            <table class="scribble-table">
              <thead>
                <tr><th>My Prediction (ProfileID)</th><th>Actual Highest (ProfileID)</th><th>Was I close? Why or why not?</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td><textarea placeholder="Your guess from earlier..."></textarea></td>
                  <td><textarea placeholder=""" + str(int(highest_profile)) + """ (auto-filled)</textarea></td>
                  <td><textarea placeholder="What attribute surprised you? What did you miss?"></textarea></td>
                </tr>
              </tbody>
            </table>
            <p style="margin-top:12px;"><strong>Next:</strong> Run the individual-level analysis to discover <em>which attributes</em> drove these ratings. The profile-level averages are just the surface.</p>
          </div>
        </div>
        """))

upload_widget.observe(on_upload_change, names='value')
display(upload_widget)
