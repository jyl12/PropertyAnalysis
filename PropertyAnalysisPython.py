# === Setup ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ===================== USER INPUTS =====================
interested_sector = []  # e.g., "Residential", "Commercial", etc.
interested_state = ["Kuala Lumpur"]  # e.g., states of interest
interested_district = ["Kuala Lumpur"]  # specific districts
interested_property_type = ["Flat", "Condominium/Apartment"]
interested_year = ["2024","2025"]
interested_tenure = []  # e.g., "Freehold", "Leasehold"

# ===================== LOAD DATA =====================
filename = r'C:\Users\Inspiron\Documents\Git\PropertyAnalysis\Open Transaction Data.csv'
data = pd.read_csv(
    filename,
    encoding='utf-16',
    sep='\t',              # Tab-delimited file
    thousands=','          # Handle numbers like 1,000 properly
)

# ===================== REFERENCE DICTIONARIES =====================
# Map sectors to property types
sector_property_type = {
    "Commercial": [
        "1 - 1 1/2 Storey Shop", "2 - 2 1/2 Storey Shop", "3 - 3 1/2 Storey Shop",
        "4 - 4 1/2 Storey Shop", "5 - 5 1/2 Storey Shop", "6 - 6 1/2 Storey Shop",
        "Condominium/Apartment", "Office Lot", "Service Apartment",
        "Shop Unit/Retail Unit", "SOHO/SOFO/SOVO"
    ],
    "Industrial": [
        "Detached Factory/Warehouse", "Industrial Unit", 
        "Semi-Detached Factory/Warehouse", "Terraced Factory/Warehouse"
    ],
    "Residential": [
        "1 - 1 1/2 Storey Semi-Detached", "1 - 1 1/2 Storey Terraced",
        "2 - 2 1/2 Storey Semi-Detached", "2 - 2 1/2 Storey Terraced",
        "Cluster House", "Condominium/Apartment", "Detached", "Flat",
        "Low-Cost Flat", "Low-Cost House", "Town House"
    ]
}

# Map states to districts
state = [
    "Johor","Kedah","Kelantan","Melaka","Negeri Sembilan","Pahang",
    "Perak","Perlis","Pulau Pinang","Sabah","Sarawak","Selangor","Terengganu",
    "WP Kuala Lumpur","WP Labuan","WP Putrajaya"
]

district = [
    ["Batu Pahat","Johor Bahru","Kluang","Kota Tinggi","Kulai","Mersing","Muar","Pontian","Segamat","Tangkak"],
    ["Baling","Bandar Baru","Kota Setar","Kuala Muda","Kubang Pasu","Kulim","Langkawi","Padang Terap","Pendang","Pokok Sena","Sik","Yan"],
    ["Bachok","Gua Musang","Jeli","Kota Bahru","Kuala Krai","Machang","Pasir Mas","Pasir Puteh","Tanah Merah","Tumpat"],
    ["Alor Gajah","Jasin","Melaka Tengah"],
    ["Jelebu","Jempoi","Kuala Pilah","Port Dickson","Rembau","Seremban","Tampin"],
    ["Bentong","Bera","Cameron Highland","Jerantut","Kuantan","Lipis","Maran","Pekan","Raub","Rompin","Temerloh"],
    ["Bagan Datuk","Batang Padang","Hilir Perak","Hulu Perak","Kampar","Kerian","Kinta","Kuala Kangsar","Larut Matang","Manjung","Mualim","Perak Tengah","Selama"],
    ["Perlis"],
    ["Barat Daya","Seberang Perai Selatan","Seberang Perai Tengah","Seberang Perai Utara","Timur Laut"],
    ["Beaufort","Keningau","Kota Belud","Kota Kinabalu","Kota Marudu","Kudat","Kunak","Labuk Sugut","Lahad Datu","Papar","Penampang","Pitas","Putatan","Ranau","Sandakan","Semporna","Sipitang","Tambunan","Tawau","Tenom","Tuaran"],
    ["Bahangian Betong","Bahagian Bintulu","Bahagian Kapit","Bahagian Kuching","Bahagian Limbang","Bahagian Miri","Bahagian Mukah","Bahagian Samarahan","Bahagian Sarikei","Bahagian Serian","Bahagian Sibu","Bahagian Sri Aman"],
    ["Gombak","Hulu Langat","Hulu Selangor","Klang","Kuala Langat","Kuala Selangor","Petaling","Sabak Bernam","Sepang"],
    ["Besut","Dungun","Hulu Terengganu","Kemaman","Kuala Nerus","Kuala Terengganu","Marang","Setiu"],
    ["Kuala Lumpur"],
    ["Labuan"],
    ["Putrajaya"]
]

state_district_dict = dict(zip(state, district))

# ===================== FILTERING DATA =====================
filtered_data = data.copy()

# Filter by state → resolve districts
if interested_state:
    all_interest_districts = []
    for s in interested_state:
        matched = [k for k in state_district_dict if s in k]
        for match in matched:
            all_interest_districts.extend(state_district_dict[match])
    filtered_data = filtered_data[filtered_data['District'].isin(all_interest_districts)]

# Filter by district
if interested_district:
    filtered_data = filtered_data[filtered_data['District'].isin(interested_district)]

# Filter by sector → resolve property types
if interested_sector:
    all_interest_property_types = []
    for s in interested_sector:
        all_interest_property_types.extend(sector_property_type.get(s, []))
    filtered_data = filtered_data[filtered_data["Property Type"].isin(all_interest_property_types)]

# Filter by specific property types
if interested_property_type:
    filtered_data = filtered_data[filtered_data["Property Type"].isin(interested_property_type)]

# Filter by year of transaction
if interested_year:
    mask = filtered_data["Month, Year of Transaction Date"].astype(str).str.contains('|'.join(interested_year))
    filtered_data = filtered_data[mask]

# Filter by tenure
if interested_tenure:
    mask = filtered_data["Tenure"].astype(str).str.contains('|'.join(interested_tenure))
    filtered_data = filtered_data[mask]

# ===================== CALCULATE PSF =====================
# Clean column names
filtered_data.columns = filtered_data.columns.str.strip()
# Clean price
price_str = filtered_data["Transaction Price"].astype(str).str.replace("RM", "").str.replace(",", "").str.strip()
price_numeric = pd.to_numeric(price_str, errors='coerce')

# Calculate PSF
land_area = pd.to_numeric(filtered_data["Land/Parcel Area"], errors='coerce')
built_up_area = pd.to_numeric(filtered_data["Main Floor Area"], errors='coerce')

filtered_data["PSF (Land/Parcel Area)"] = price_numeric / (land_area * 10.7639)
filtered_data["PSF (Main Floor Area)"] = price_numeric / (built_up_area * 10.7639)

# ===================== VISUALIZATION =====================

# Boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=filtered_data, x="Property Type", y="PSF (Land/Parcel Area)")
plt.xticks(rotation=45, ha='right')
plt.title("Price Per Square Foot (Land/Parcel Area) by Property Type")
plt.ylabel("PSF (RM)")
plt.xlabel("Property Type")
plt.tight_layout()
plt.show()

# Histogram
plt.figure(figsize=(10, 5))
valid = filtered_data["PSF (Land/Parcel Area)"].dropna()
plt.hist(valid, bins=50)
plt.xlabel("Price Per Square Foot (Land/Parcel Area)")
plt.ylabel("Number of Transactions")
plt.title("Distribution of Property Prices per Square Foot")
plt.tight_layout()
plt.show()

# Scatter Plot
valid_data = filtered_data.dropna(subset=["Land/Parcel Area", "PSF (Land/Parcel Area)", "Property Type"])
plt.figure(figsize=(10, 6))
sns.scatterplot(data=valid_data, x="Land/Parcel Area", y="PSF (Land/Parcel Area)", hue="Property Type")
plt.xlabel("Land/Parcel Area (m²)")
plt.ylabel("Price Per Square Foot (Land/Parcel Area)")
plt.title("Property Size vs. Price per Square Foot")
plt.tight_layout()
plt.show()
