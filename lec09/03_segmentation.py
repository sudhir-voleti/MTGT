# ═══════════════════════════════════════════════════════════════════
#  STEP 3: Segmentation — K-Means on Part-Worths + Psychographic Validation
# ═══════════════════════════════════════════════════════════════════

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --- 1. K-Means on part-worths ---
print("="*60)
print("K-MEANS SEGMENTATION ON PART-WORTHS")
print("="*60)

pw_matrix = ib_df[['Range_110', 'Range_150', 'Charge_fast', 'Price_85', 'Price_110',
                   'Service_100', 'Service_300', 'Smart_Adv', 'Warr_4', 'Warr_6']].fillna(0).values

scaler = StandardScaler()
pw_scaled = scaler.fit_transform(pw_matrix)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(pw_scaled)

ib_df['Cluster'] = clusters

# Map clusters to meaningful names (dominant segment in each cluster)
cluster_seg = pd.crosstab(ib_df['Cluster'], metric_df.groupby('RespID')['Segment'].first())
print("\nCluster vs True Segment:")
print(cluster_seg)

# Auto-name clusters based on dominant true segment
cluster_names = {}
for c in sorted(ib_df['Cluster'].unique()):
    true_segs = metric_df[metric_df['RespID'].isin(ib_df[ib_df['Cluster']==c]['RespID'])]['Segment']
    cluster_names[c] = true_segs.value_counts().index[0]

ib_df['ClusterName'] = ib_df['Cluster'].map(cluster_names)
print(f"\nAuto-named clusters: {cluster_names}")

# --- 2. Psychographic validation ---
print("\n" + "="*60)
print("PSYCHOGRAPHIC VALIDATION")
print("="*60)

# Merge psychographic data with clusters
psych_clusters = psych_df.merge(ib_df[['RespID', 'Cluster', 'ClusterName']], on='RespID', how='left')

print("\nPsychographic means by CLUSTER:")
psych_by_cluster = psych_clusters.groupby('ClusterName')[['TechEnthusiasm', 'PriceSensitivity', 
                                                          'RiskAversion', 'EnvironmentalMotiv', 
                                                          'UrbanCommuteStress']].mean()
print(psych_by_cluster.round(2))

print("\nPsychographic means by TRUE SEGMENT:")
psych_by_true = psych_df.groupby('Segment')[['TechEnthusiasm', 'PriceSensitivity', 
                                              'RiskAversion', 'EnvironmentalMotiv', 
                                              'UrbanCommuteStress']].mean()
print(psych_by_true.round(2))

# --- 3. Plot: Attribute importance by cluster ---
fig, ax = plt.subplots(figsize=(10, 6))

imp_clusters = importance.copy()
imp_clusters['Cluster'] = ib_df['ClusterName'].values
imp_by_cluster = imp_clusters.groupby('Cluster')[['Range', 'Charge', 'Price', 'Service', 'Smart', 'Warranty']].mean()

x = np.arange(6)
w = 0.25
colors = ['#2c7a7b', '#d69e2e', '#e53e3e']

for i, (cluster, color) in enumerate(zip(imp_by_cluster.index, colors)):
    ax.bar(x + i*w, imp_by_cluster.loc[cluster], w, label=cluster, color=color, edgecolor='black')

ax.set_xticks(x + w)
ax.set_xticklabels(['Range', 'Charge', 'Price', 'Service', 'Smart', 'Warranty'])
ax.set_ylabel('Importance (%)')
ax.set_title('Attribute Importance by Cluster')
ax.legend()
ax.set_ylim(0, 50)
plt.tight_layout()
plt.show()

print("\n✅ Clusters stored in ib_df['ClusterName'] for Step 4 (CBC)")
