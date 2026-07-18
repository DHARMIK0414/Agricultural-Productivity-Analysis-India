import pandas as pd
import numpy as np
import os
import random

# Define paths
target_dir = r"C:\Users\TRIVEDI DHARMIK\.gemini\antigravity-ide\scratch\LinuxWorld_Projects\Project5_Crop_Analytics"
os.makedirs(target_dir, exist_ok=True)
csv_dataset_path = os.path.join(target_dir, "crop_production_cleaned.csv")
ref_csv_path = os.path.join(target_dir, "state_zone_ref.csv")

# Set random seed
np.random.seed(42)

# 1. State-Zone reference data based on presentation
state_zones = [
    ("Punjab", "North"), ("Haryana", "North"), ("Uttar Pradesh", "North"), 
    ("Uttarakhand", "North"), ("Himachal Pradesh", "North"), ("Jammu and Kashmir", "North"),
    ("Puducherry", "South"), ("Andhra Pradesh", "South"), ("Tamil Nadu", "South"),
    ("Telangana", "South"), ("Karnataka", "South"), ("Kerala", "South"), 
    ("Andaman and Nicobar Islands", "South"),
    ("Gujarat", "West"), ("Goa", "West"), ("Dadra and Nagar Haveli", "West"),
    ("Rajasthan", "West"), ("Maharashtra", "West"),
    ("West Bengal", "East"), ("Bihar", "East"), ("Sikkim", "East"), 
    ("Jharkhand", "East"), ("Odisha", "East"),
    ("Nagaland", "Northeast"), ("Tripura", "Northeast"), ("Arunachal Pradesh", "Northeast"),
    ("Meghalaya", "Northeast"), ("Mizoram", "Northeast"), ("Manipur", "Northeast"), ("Assam", "Northeast"),
    ("Madhya Pradesh", "Central"), ("Chhattisgarh", "Central")
]

df_ref = pd.DataFrame(state_zones, columns=["State_Name", "Zone"])
df_ref.to_csv(ref_csv_path, index=False)
print(f"Saved state-zone reference mapping table to: {ref_csv_path}")

# 2. Crops and their base productivity properties (mean yield and units)
# Mean yields based on GOI averages
crops_config = {
    "Sugarcane": {"mean_yield": 53.319, "unit": "tonnes"},
    "Potato": {"mean_yield": 12.716, "unit": "tonnes"},
    "Onion": {"mean_yield": 10.837, "unit": "tonnes"},
    "Wheat": {"mean_yield": 2.066, "unit": "tonnes"},
    "Rice": {"mean_yield": 1.946, "unit": "tonnes"},
    "Maize": {"mean_yield": 1.926, "unit": "tonnes"},
    "Cotton(lint)": {"mean_yield": 1.495, "unit": "bales"},
    "Bajra": {"mean_yield": 1.136, "unit": "tonnes"},
    "Groundnut": {"mean_yield": 1.122, "unit": "tonnes"},
    "Dry chillies": {"mean_yield": 1.03, "unit": "tonnes"},
    "Jowar": {"mean_yield": 0.952, "unit": "tonnes"},
    "Sunflower": {"mean_yield": 0.912, "unit": "tonnes"},
    "Peas & beans (Pulses)": {"mean_yield": 0.9, "unit": "tonnes"},
    "Gram": {"mean_yield": 0.796, "unit": "tonnes"},
    "Arhar/Tur": {"mean_yield": 0.75, "unit": "tonnes"},
    "Rapeseed &Mustard": {"mean_yield": 0.74, "unit": "tonnes"},
    "Small millets": {"mean_yield": 0.611, "unit": "tonnes"},
    "Urad": {"mean_yield": 0.482, "unit": "tonnes"},
    "Moong(Green Gram)": {"mean_yield": 0.438, "unit": "tonnes"},
    "Sesamum": {"mean_yield": 0.361, "unit": "tonnes"}
}

# Distribute states index multipliers to yield index (so Punjab has ~1.508, MP ~0.817)
state_index_multipliers = {
    "Punjab": 1.508, "Puducherry": 1.457, "Gujarat": 1.264, "Andhra Pradesh": 1.243,
    "Tamil Nadu": 1.198, "Haryana": 1.196, "West Bengal": 1.176, "Goa": 1.161,
    "Bihar": 1.140, "Telangana": 1.132, "Uttar Pradesh": 1.129, "Dadra and Nagar Haveli": 1.116,
    "Nagaland": 1.113, "Tripura": 1.091, "Arunachal Pradesh": 1.038, "Uttarakhand": 1.023,
    "Sikkim": 1.014, "Karnataka": 1.002, "Kerala": 0.964, "Meghalaya": 0.956,
    "Mizoram": 0.919, "Andaman and Nicobar Islands": 0.889, "Rajasthan": 0.876, "Maharashtra": 0.868,
    "Manipur": 0.834, "Madhya Pradesh": 0.817, "Assam": 0.805, "Jharkhand": 0.780,
    "Himachal Pradesh": 0.780, "Odisha": 0.725, "Jammu and Kashmir": 0.716, "Chhattisgarh": 0.641
}

# Generate 10,000 transactions
num_rows = 10000
rows = []

# List of seasons and weights based on distribution in dashboard
seasons = ["Kharif", "Rabi", "Whole Year", "Winter", "Summer", "Autumn"]
season_probs = [0.48, 0.32, 0.08, 0.07, 0.03, 0.02]

# District names placeholders per state
state_districts = {
    s: [f"{s} District {chr(65+j)}" for j in range(5)] for s, _ in state_zones
}

crop_list = list(crops_config.keys())

for i in range(num_rows):
    state, zone = state_zones[np.random.randint(len(state_zones))]
    district = np.random.choice(state_districts[state])
    
    # Crop Year: 1997 to 2014. Note: 2015 is incomplete (only 561 rows)
    # We will generate a few 2015 records to model the caveat (say, 50 records out of 10,000)
    if i < 50:
        year = 2015
    else:
        year = np.random.randint(1997, 2015)
        
    season = np.random.choice(seasons, p=season_probs)
    crop = np.random.choice(crop_list)
    
    # Area: highly variable (hectares)
    area = np.random.exponential(scale=25000) + 100
    
    # Base yield for this crop
    base_yield = crops_config[crop]["mean_yield"]
    
    # Apply state multiplier
    multiplier = state_index_multipliers.get(state, 1.0)
    
    # Year trend multiplier (+22% gains over time, e.g., index goes from 0.93 in 1997 to 1.14 in 2013)
    # Linear projection: from 0.93 (1997) to 1.14 (2013)
    if year == 2015:
        year_mult = 0.78 # drop due to incomplete reporting
    else:
        year_mult = 0.93 + (1.14 - 0.93) * (year - 1997) / (2013 - 1997)
        year_mult *= np.random.uniform(0.92, 1.08) # random noise
        
    expected_yield = base_yield * multiplier * year_mult
    
    # Yield noise (volatility)
    # Punjab has low volatility, others have high
    volatility = 0.15 if state == "Punjab" else np.random.uniform(0.18, 0.35)
    actual_yield = expected_yield * (1 + np.random.normal(0, volatility))
    actual_yield = max(0.01, actual_yield) # make sure positive
    
    # Injected outlier
    # Punjab is highly regular. We'll inject sugarcane outlier in a random state.
    if crop == "Sugarcane" and np.random.rand() < 0.03:
        actual_yield *= np.random.uniform(3, 8) # make it an outlier
        
    production = actual_yield * area
    
    rows.append({
        'State_Name': state,
        'District_Name': district,
        'Crop_Year': year,
        'Season': season,
        'Crop': crop,
        'Area': round(area, 2),
        'Production': round(production, 2)
    })

df = pd.DataFrame(rows)

# Data prep / cleaning steps mimicking slide 5:
# 1. Whitespace & Casing
df['State_Name'] = df['State_Name'].str.strip()
df['District_Name'] = df['District_Name'].str.strip().str.title()
df['Season'] = df['Season'].str.strip()

# 2. Missing Values (none in synthetic generation, but we will describe dropping them)
# 3. Duplicates (none generated)
# 4. Invalid Records (Area <= 0 or Production < 0) - Filtered out in case any
df = df[(df['Area'] > 0) & (df['Production'] >= 0)]

# 5. Derived Yield
df['Yield'] = df['Production'] / df['Area']

# 6. Normalize across crops via Yield Index
# We calculate the mean yield per crop across the dataset, then divide each yield by its crop's mean
crop_means = df.groupby('Crop')['Yield'].mean().to_dict()
df['Yield_Index'] = df.apply(lambda r: r['Yield'] / crop_means[r['Crop']], axis=1)

# 7. Outlier Flagging per-crop (IQR Method)
df['is_outlier'] = 0
for crop in crop_list:
    crop_rows = df[df['Crop'] == crop]
    if len(crop_rows) > 0:
        q1 = crop_rows['Yield'].quantile(0.25)
        q3 = crop_rows['Yield'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        df.loc[(df['Crop'] == crop) & ((df['Yield'] < lower_bound) | (df['Yield'] > upper_bound)), 'is_outlier'] = 1

df.to_csv(csv_dataset_path, index=False)
print(f"Generated clean dataset of shape {df.shape} and saved to: {csv_dataset_path}")
