# === Setup ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ===================== USER INPUTS =====================
interested_sector = []  # e.g., "Residential", "Commercial", etc.
interested_state = ["Kuala Lumpur"]  # e.g., states of interest
interested_district = ["Kuala Lumpur"]  # specific districts
interested_property_type = ["1 - 1 1/2 Storey Shop","Flat"]
interested_year = ["2024","2025"]
interested_tenure = []  # e.g., "Freehold", "Leasehold"

# ===================== LOAD DATA =====================
filename = r'C:\Users\Inspiron\Documents\Git\RealEstateAnalysis\Open Transaction Data.csv'
data = pd.read_csv(
    filename,
    encoding='utf-16',
    sep='\t',              # Tab-delimited file
    thousands=',',          # Handle numbers like 1,000 properly
    low_memory=False
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
# First dataset: PSF (Land)
psf_land = filtered_data[["Property Type","PSF (Land/Parcel Area)"]].dropna()
# Second dataset: PSF (Built-up)
psf_built = filtered_data[["Property Type","PSF (Main Floor Area)"]].dropna()

# Boxplot
# Count how many plots to create
n_subplots = 1 + int(not psf_built.empty)

# Create subplots
fig, axes = plt.subplots(1, n_subplots, figsize=(8 * n_subplots, 6), sharey=True)
if n_subplots == 1:
    axes = [axes]

# First subplot: PSF (Land Area)
sns.boxplot(data=psf_land, x="Property Type", y="PSF (Land/Parcel Area)", ax=axes[0])
axes[0].set_title("Price per Square Foot (Land/Parcel Area) by Property Type")
axes[0].set_xlabel("Property Type")
axes[0].set_ylabel("Price per Square Foot")
axes[0].tick_params(axis='x', rotation=45)

# Second subplot: PSF (Built-up Area), only if data exists
if not psf_built.empty:
    sns.boxplot(data=psf_built, x="Property Type", y="PSF (Main Floor Area)", ax=axes[1])
    axes[1].set_title("Price per Square Foot (Built-up Area) by Property Type ")
    axes[1].set_xlabel("Property Type")
    axes[1].set_ylabel("Price per Square Foot")
    axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# Histogram
n_subplots = 1 + int(not psf_built.empty)

fig, axes = plt.subplots(1, n_subplots, figsize=(10 * n_subplots, 5), sharey=True)
if n_subplots == 1:
    axes = [axes]
# First subplot: PSF (Land Area)
valid = filtered_data["PSF (Land/Parcel Area)"].dropna()
axes[0].hist(valid, bins=50)
axes[0].set_title("Distribution of Property Prices per Square Foot")
axes[0].set_xlabel("Price Per Square Foot (Land/Parcel Area)")
axes[0].set_ylabel("Number of Transactions")

# Second subplot: PSF (Built-up Area), only if data exists
if not psf_built.empty:
    valid = filtered_data["PSF (Main Floor Area)"].dropna()
    axes[1].hist(valid,  bins=50)
    axes[1].set_title("Distribution of Property Prices per Square Foot")
    axes[1].set_xlabel("Price Per Square Foot (Main Floor Area)")
    axes[1].set_ylabel("Number of Transactions")

plt.tight_layout()
plt.show()

# Scatter Plot
# Filter valid data for Land/Parcel Area PSF
valid_land = filtered_data.dropna(subset=["Land/Parcel Area", "PSF (Land/Parcel Area)", "Property Type"])

# Filter valid data for Main Floor Area PSF (if exists)
valid_built = filtered_data.dropna(subset=["Main Floor Area", "PSF (Main Floor Area)", "Property Type"])

# Determine how many subplots (1 or 2)
n_plots = 1 + int(not valid_built.empty)

fig, axes = plt.subplots(1, n_plots, figsize=(10 * n_plots, 6), sharey=True)

# If only one subplot, axes is not a list, make it one for uniformity
if n_plots == 1:
    axes = [axes]

# Plot 1: Land/Parcel Area PSF scatter
sns.scatterplot(
    data=valid_land,
    x="Land/Parcel Area",
    y="PSF (Land/Parcel Area)",
    hue="Property Type",
    alpha=0.7,
    ax=axes[0]
)
axes[0].set_title("Land/Parcel Area vs Price per Square Foot")
axes[0].set_xlabel("Land/Parcel Area")
axes[0].set_ylabel("Price Per Square Foot (Land/Parcel Area)")

# Plot 2: Main Floor Area PSF scatter (if data available)
if n_plots == 2:
    sns.scatterplot(
        data=valid_built,
        x="Main Floor Area",
        y="PSF (Main Floor Area)",
        hue="Property Type",
        alpha=0.7,
        ax=axes[1]
    )
    axes[1].set_title("Main Floor Area vs Price per Square Foot")
    axes[1].set_xlabel("Main Floor Area")
    axes[1].set_ylabel("Price Per Square Foot (Land/Parcel Area)")

plt.tight_layout()
plt.show()
