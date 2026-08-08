# ═══════════════════════════════════════════════════════════════════
#  STEP 1: Upload & Profile
# ═══════════════════════════════════════════════════════════════════

# Auto-load from GitHub (no upload needed if files are in repo)
print("Loading Yana data files from GitHub …")

metric_df = pd.read_csv(requests.get(BASE + "yana_metric_conjoint_n400.csv").content)
cbc_df = pd.read_csv(requests.get(BASE + "yana_cbc_n400.csv").content)
psych_df = pd.read_csv(requests.get(BASE + "yana_psychographic_n400.csv").content)
profiles = pd.read_csv(requests.get(BASE + "yana_profiles_16.csv").content)

print(f"✅ Metric conjoint: {len(metric_df)} rows ({metric_df['RespID'].nunique()} respondents × {metric_df['ProfileID'].nunique()} profiles)")
print(f"✅ CBC: {len(cbc_df)} rows ({cbc_df['RespID'].nunique()} respondents × {cbc_df['Task'].nunique()} tasks)")
print(f"✅ Psychographic: {len(psych_df)} rows × {len([c for c in psych_df.columns if c not in ['RespID','Segment']])} items")
print(f"✅ Design profiles: {len(profiles)} profiles")

# Display structure
print("\n--- Metric Conjoint Sample ---")
display(metric_df.head(8))

print("\n--- CBC Sample (one task) ---")
display(cbc_df[cbc_df['RespID'] == 1].head(8))

print("\n--- Psychographic Sample ---")
display(psych_df.head())

print("\n--- Profile Design ---")
display(profiles)

# Summary stats
print("\n--- Rating Distribution ---")
print(metric_df['Rating'].value_counts().sort_index())

print("\n--- None Choice Rate ---")
none_rate = cbc_df[(cbc_df['AltID'] == 4) & (cbc_df['Chosen'] == 1)].shape[0] / cbc_df['Task'].nunique() / cbc_df['RespID'].nunique()
print(f"Overall: {none_rate:.1%}")

print("\n--- Psychographic Means by Segment (true labels) ---")
if 'Segment' in psych_df.columns:
    print(psych_df.groupby('Segment')[['TechEnthusiasm', 'PriceSensitivity', 'RiskAversion', 'EnvironmentalMotiv', 'UrbanCommuteStress']].mean().round(2))
