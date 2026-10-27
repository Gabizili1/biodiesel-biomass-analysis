import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor

# =====================================================================
# 🎓 M.Sc. THESIS COMPUTATIONAL MODEL: BIODIESEL PROPERTIES & VISUALIZATION
# =====================================================================
print("Initializing M.Sc. Thesis Data Engineering Pipeline...")

# 1. PROGRAMMATIC DATA INGESTION
# Populated using verified quantitative metrics from your published paper
data_matrix = {
    'Feedstock': ['Beef Tallow', 'Avocado Seed Pulp', 'Watermelon Seeds', 'Balanite Kernel'],
    'Oil_Yield_Pct': [92.80, 10.96, 20.02, 39.65],
    'Kinematic_Viscosity': [4.92, 5.02, 3.70, 5.42],
    'Density': [0.87, 0.93, 0.86, 1.33],
    'Acid_Value': [0.28, 0.84, 3.09, 0.56],
    'Flash_Point': [154.0, 172.0, 102.0, 172.0],
    'Cloud_Point': [-8.0, -5.0, -2.0, -13.0],
    'Biodiesel_Yield_Pct': [87.40, 81.92, 57.24, 92.03]  # Target metric
}

df = pd.DataFrame(data_matrix)
print("\n[✔] Data Ingested Successfully:")
print(df[['Feedstock', 'Oil_Yield_Pct', 'Biodiesel_Yield_Pct']])

# 2. MACHINE LEARNING ARCHITECTURE SETUP
X = df[['Oil_Yield_Pct', 'Kinematic_Viscosity', 'Density', 'Acid_Value', 'Flash_Point', 'Cloud_Point']]
y = df['Biodiesel_Yield_Pct']

# Fit model on baseline parameters
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X, y)
print("\n[✔] Machine Learning Training Cycle Complete (Random Forest Fitted).")

# 3. STATISTICAL CORRELATION HEATMAP PRODUCTION
print("\n[✔] Computing Statistical Feature Engineering Matrices...")
plt.figure(figsize=(8, 6))

# Drop non-numeric column for mathematical correlation mapping
numeric_df = df.drop(columns=['Feedstock'])
correlation_matrix = numeric_df.corr()

# Construct the custom visualization matrix layout
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('M.Sc. Thesis Analytics: Biomass Property Correlation Matrix', fontsize=12, pad=15)
plt.tight_layout()

# Save image file directly to your workspace repository layout
heatmap_filename = "biomass_property_correlation_matrix.png"
plt.savefig(heatmap_filename, dpi=300)
print(f"-> Generated Publication Graph Saved Exclusively As: {heatmap_filename}")

# 4. AUTOMATED COMPLIANCE SIMULATOR (ASTM D6751 / EN 14214 Verification)
def evaluate_blend_compliance(viscosity, flash_point):
    """
    Flags whether an engineered biomass blend meets standard criteria boundaries.
    """
    visc_ok = 1.9 <= viscosity <= 6.0
    flash_ok = flash_point >= 130
    return "PASS (Compliant with Standard Regulation)" if (visc_ok and flash_ok) else "FAIL (Requires B20 Blending / Refinement)"

print("\n--- Programmatic Quality Assurance Check (Simulated Pure Variants) ---")
for idx, row in df.iterrows():
    status = evaluate_blend_compliance(row['Kinematic_Viscosity'], row['Flash_Point'])
    print(f"-> Feedstock: {row['Feedstock']} | Compliance Status: {status}")
