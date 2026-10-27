import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor

print("Initializing Biodiesel Data Engineering Pipeline...")

# Define paths relative to the current workspace
yields_path = "data/raw_yields.csv"
props_path = "data/physicochemical_properties.csv"

# 1. VERIFY FILE ARCHITECTURE AND INGEST DATA DYNAMICALLY
if not os.path.exists(yields_path) or not os.path.exists(props_path):
    print("\n[X] Error: Data files missing from the /data directory.")
    print("Please ensure raw_yields.csv and physicochemical_properties.csv exist.")
    exit(1)

# Ingest structured datasets into Pandas DataFrames
yields_df = pd.read_csv(yields_path)
props_df = pd.read_csv(props_path)

# Restructure the matrix from long format to a wide column layout for machine learning
melted_props = props_df.set_index('Parameter').T
melted_props = melted_props.reset_index().rename(columns={'index': 'Feedstock_Key'})

# Map shorthand labels back to unified full names for merging
feedstock_mapping = {
    'Avocado_B100': 'Avocado Seed Pulp',
    'Watermelon_B100': 'Watermelon Seeds',
    'Balanite_B100': 'Balanite Kernel',
    'Beef_Tallow_B100': 'Beef Tallow Fat'
}
melted_props['Feedstock'] = melted_props['Feedstock_Key'].map(feedstock_mapping)

# Standardize names in the yields file to match
yields_mapping = {
    'Avocado Seed Pulp': 'Avocado Seed Pulp',
    'Watermelon Seeds': 'Watermelon Seeds',
    'Balanite Kernel': 'Balanite Kernel',
    'Beef Tallow Fat': 'Beef Tallow Fat'
}
yields_df['Feedstock'] = yields_df['Feedstock'].map(yields_mapping)

# Merge datasets into a unified analytical matrix
df = pd.merge(yields_df, melted_props, on='Feedstock').dropna(subset=['Feedstock'])
df = df.apply(pd.to_numeric, errors='ignore')

print("\n[✔] Structural Dataset Ingested and Merged Successfully:")
print(df[['Feedstock', 'Average_Oil_Yield_Percent', 'Average_Biodiesel_Yield_Percent']])

# 2. PREDICTIVE MODEL CONFIGURATION
features = ['Average_Oil_Yield_Percent', 'Kinematic_Viscosity_mm2_s', 'Density_g_cm3', 'Acid_Value_mgKOH_g', 'Flash_Point_C', 'Cloud_Point_C']
X = df[features]
y = df['Average_Biodiesel_Yield_Percent']

# Fit regression model on parameters
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X, y)
print("\n[✔] Machine Learning Training Cycle Complete (Random Forest Fitted).")

# 3. STATISTICAL CORRELATION HEATMAP PRODUCTION
print("\n[✔] Computing Statistical Feature Engineering Matrices...")
plt.figure(figsize=(8, 6))

numeric_df = df[features + ['Average_Biodiesel_Yield_Percent']]
correlation_matrix = numeric_df.corr()

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Biomass Property Correlation Matrix', fontsize=12, pad=15)
plt.tight_layout()

heatmap_filename = "biomass_property_correlation_matrix.png"
plt.savefig(heatmap_filename, dpi=300)
print(f"-> Generated Analysis Graph Saved As: {heatmap_filename}")

# 4. AUTOMATED COMPLIANCE SIMULATOR (ASTM D6751 Verification)
def evaluate_blend_compliance(viscosity, flash_point):
    visc_ok = 1.9 <= viscosity <= 6.0
    flash_ok = flash_point >= 130
    return "PASS (Compliant with Standard Regulation)" if (visc_ok and flash_ok) else "FAIL (Requires B20 Blending / Refinement)"

print("\n--- Programmatic Quality Assurance Check (Pure Variants) ---")
for idx, row in df.iterrows():
    status = evaluate_blend_compliance(row['Kinematic_Viscosity_mm2_s'], row['Flash_Point_C'])
    print(f"-> Feedstock: {row['Feedstock']} | Compliance Status: {status}")
