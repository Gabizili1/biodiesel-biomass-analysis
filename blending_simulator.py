import os
import pandas as pd

print("=====================================================================")
print("     AUTOMATED MULTI-FEEDSTOCK BIODIESEL BLENDING SIMULATOR          ")
print("=====================================================================")

props_path = "data/physicochemical_properties.csv"

# 1. VERIFY ASSETS AND LOADING
if not os.path.exists(props_path):
    print(f"[X] Error: Baseline property definitions missing at '{props_path}'")
    exit(1)

props_df = pd.read_csv(props_path)
melted_props = props_df.set_index('Parameter').T

# Define exact mathematical blend target options from matching dataframe indexes
feedstock_mapping = {
    'Avocado_B100': 'Avocado Seed Pulp',
    'Watermelon_B100': 'Watermelon Seeds',
    'Balanite_B100': 'Balanite Kernel',
    'Beef_Tallow_B100': 'Beef Tallow Fat'
}
melted_props.index = melted_props.index.map(feedstock_mapping)

# 2. DEFINE VARIABLE MULTI-FEEDSTOCK BLENDING PROPORTIONS
# Ensure total ratio metrics sum up to 1.0 (100% Volume)
# Updated optimized metrics layout: Low Balanite, High Watermelon & Tallow
blend_ratios = {
    'Beef Tallow Fat': 0.45,       # 45% Volume (Compliant baseline)
    'Balanite Kernel': 0.05,       # 5% Volume (Dropped drastically to fix density)
    'Watermelon Seeds': 0.40,      # 40% Volume (Increased to lighten the blend)
    'Avocado Seed Pulp': 0.10      # 10% Volume
}


# Verification check for volume metrics integrity
if not abs(sum(blend_ratios.values()) - 1.0) < 1e-9:
    print("[X] Error: Volumetric blending proportions must sum up to exactly 1.0 (100%)")
    exit(1)

print("\nActive Volumetric Mixture Configurations:")
for feedstock, ratio in blend_ratios.items():
    print(f" -> {feedstock}: {ratio * 100:.1f}%")

# 3. INTERPOLATE PHYSIOCHEMICAL BLEND MATRIX CALCULATIONS
simulated_density = 0.0
simulated_viscosity = 0.0
simulated_flash = 0.0
simulated_cloud = 0.0

for feedstock, ratio in blend_ratios.items():
    simulated_density += melted_props.loc[feedstock, 'Density_g_cm3'] * ratio
    simulated_viscosity += melted_props.loc[feedstock, 'Kinematic_Viscosity_mm2_s'] * ratio
    simulated_flash += melted_props.loc[feedstock, 'Flash_Point_C'] * ratio
    simulated_cloud += melted_props.loc[feedstock, 'Cloud_Point_C'] * ratio

print("\n=====================================================================")
print("                   COMPUTED BLEND ANALYSIS RESULTS                   ")
print("=====================================================================")
print(f" -> Calculated Mixture Density   : {simulated_density:.3f} g/cm³")
print(f" -> Calculated Kinematic Viscosity: {simulated_viscosity:.2f} mm²/s")
print(f" -> Calculated Core Flash Point  : {simulated_flash:.1f} °C")
print(f" -> Calculated Target Cloud Point: {simulated_cloud:.1f} °C")

# 4. REGULATORY REGIME ASSESSMENT PIPELINE (ASTM D6751 / EN 14214 standard check)
print("\n=====================================================================")
print("                INTERNATIONAL FUEL COMPLIANCE METRICS                ")
print("=====================================================================")

# Limits checking logic
visc_ok = 1.9 <= simulated_viscosity <= 6.0
density_ok = 0.86 <= simulated_density <= 0.90
flash_ok = simulated_flash >= 130

print(f" -> Kinematic Viscosity Status (1.9 - 6.0) : {'[ PASS ]' if visc_ok else '[ FAIL ]'}")
print(f" -> Density Matrix Status (0.86 - 0.90)    : {'[ PASS ]' if density_ok else '[ FAIL ]'}")
print(f" -> Minimum Flash Safety Status (>= 130°C) : {'[ PASS ]' if flash_ok else '[ FAIL ]'}")

if visc_ok and density_ok and flash_ok:
    print("\nResult: COMPLIANT MIXTURE. Ready for hardware performance evaluations.")
else:
    print("\nResult: NON-COMPLIANT MIXTURE. Adjust feedstock volume allocations.")
