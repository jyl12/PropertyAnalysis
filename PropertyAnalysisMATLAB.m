clear all; clc; close all;  % Clear workspace, command window, and close all figures

% ===================== USER INPUTS =====================
% Define filters to apply on the dataset
interestedSector = [];  % e.g., "Residential", "Commercial", etc.
interestedState = ["Kuala Lumpur"];  % e.g., states of interest
interestedDistrict = [];  % specific districts if any
interestedPropertyType = ["Condominium/Apartment","Service Apartment"];  % types of property to filter
interestedYear = ["2024"];  % year(s) of transaction
interestedTenure = [];  % e.g., "Freehold", "Leasehold"

% ===================== LOAD DATA =====================
% Path to the CSV file containing transaction data
% Source: https://napic2.jpph.gov.my/en/open-sales-data?category=36&id=241
filename = 'Open Transaction Data.csv';

% Read the CSV file into a table while preserving original variable names
data = readtable(filename,"VariableNamingRule","preserve");

% ===================== REFERENCE DICTIONARIES =====================
% Define mapping of sectors to property types
sector = ["Commercial","Industrial","Residential"];
propertyType = {
    ["1 - 1 1/2 Storey Shop","2 - 2 1/2 Storey Shop","3 - 3 1/2 Storey Shop","4 - 4 1/2 Storey Shop","5 - 5 1/2 Storey Shop","6 - 6 1/2 Storey Shop","Condominium/Apartment","Office Lot","Service Apartment","Shop Unit/Retail Unit","SOHO/SOFO/SOVO"],...
    ["Detached Factory/Warehouse","Industrial Unit","Semi-Detached Factory/Warehouse","Terraced Factory/Warehouse"],...
    ["1 - 1 1/2 Storey Semi-Detached","1 - 1 1/2 Storey Terraced","2 - 2 1/2 Storey Semi-Detached","2 - 2 1/2 Storey Terraced","Cluster House","Condominium/Apartment","Detached","Flat","Low-Cost Flat","Low-Cost House","Town House"]
};

% Define mapping of states to districts
state = ["Johor","Kedah","Kelantan","Melaka","Negeri Sembilan","Pahang",...
    "Perak","Perlis","Pulau Pinang","Sabah","Sarawak","Selangor","Terengganu",...
    "WP Kuala Lumpur","WP Labuan","WP Putrajaya"];

district = {... % Each element corresponds to the state at the same index
    ["Batu Pahat","Johor Bahru","Kluang","Kota Tinggi","Kulai","Mersing","Muar","Pontian","Segamat","Tangkak"],...
    ["Baling","Bandar Baru","Kota Setar","Kuala Muda","Kubang Pasu","Kulim","Langkawi","Padang Terap","Pendang","Pokok Sena","Sik","Yan"],...
    ["Bachok","Gua Musang","Jeli","Kota Bahru","Kuala Krai","Machang","Pasir Mas","Pasir Puteh","Tanah Merah","Tumpat"],...
    ["Alor Gajah","Jasin","Melaka Tengah"],...
    ["Jelebu","Jempoi","Kuala Pilah","Port Dickson","Rembau","Seremban","Tampin"],...
    ["Bentong","Bera","Cameron Highland","Jerantut","Kuantan","Lipis","Maran","Pekan","Raub","Rompin","Temerloh"],...
    ["Bagan Datuk","Batang Padang","Hilir Perak","Hulu Perak","Kampar","Kerian","Kinta","Kuala Kangsar","Larut Matang","Manjung","Mualim","Perak Tengah","Selama"],...
    "Perlis",...
    ["Barat Daya","Seberang Perai Selatan","Seberang Perai Tengah", "Seberang Perai Utara","Timur Laut"],...
    ["Beaufort","Keningau","Kota Belud","Kota Kinabalu","Kota Marudu","Kudat","Kunak","Labuk Sugut","Lahad Datu","Papar","Penampang","Pitas","Putatan","Ranau","Sandakan","Semporna","Sipitang","Tambunan","Tawau","Tenom","Tuaran"],...
    ["Bahangian Betong","Bahagian Bintulu","Bahagian Kapit","Bahagian Kuching","Bahagian Limbang","Bahagian Miri","Bahagian Mukah","Bahagian Samarahan","Bahagian Sarikei","Bahagian Serian","Bahagian Sibu","Bahagian Sri Aman"],...
    ["Gombak","Hulu Langat","Hulu Selangor","Klang","Kuala Langat","Kuala Selangor","Petaling","Sabak Bernam","Sepang"],...
    ["Besut","Dungun","Hulu Terengganu","Kemaman","Kuala Nerus","Kuala Terengganu","Marang","Setiu"],...
    "Kuala Lumpur",...
    "Labuan",...
    "Putrajaya"
};

% Create dictionaries for fast lookup
stateDistrictDict = dictionary(state,district);
sectorPropertyTypeDict = dictionary(sector,propertyType);

% ===================== FILTERING DATA =====================
filteredData = data;

% Filter by state → resolve to all districts in selected states
if ~isempty(interestedState)
    key = find(contains(state,interestedState));
    interestDistrict = stateDistrictDict(state(key));
    allInterestDistricts = string([interestDistrict{:}]);

    rows = ismember(data.District, allInterestDistricts);
    filteredData = data(rows, :);
end

% Filter by district (if explicitly specified)
if ~isempty(interestedDistrict)
    rows = ismember(filteredData.District, interestedDistrict);
    filteredData = filteredData(rows, :);
end

% Filter by sector → resolve to property types under that sector
if ~isempty(interestedSector)
    key = find(contains(sector,interestedSector));
    interestPropertyType = sectorPropertyTypeDict(sector(key));
    allInterestPropertyTypes = string([interestPropertyType{:}]);

    rows = ismember(filteredData.("Property Type"), allInterestPropertyTypes);
    filteredData = filteredData(rows, :);
end

% Filter by specific property types
if ~isempty(interestedPropertyType)
    rows = ismember(filteredData.("Property Type"), interestedPropertyType);
    filteredData = filteredData(rows, :);
end

% Filter by year of transaction
if ~isempty(interestedYear)
    rows = contains(filteredData.("Month, Year of Transaction Date"), interestedYear);
    filteredData = filteredData(rows, :);
end

% Filter by tenure type
if ~isempty(interestedTenure)
    rows = contains(filteredData.Tenure, interestedTenure);
    filteredData = filteredData(rows, :);
end

% ===================== CALCULATE PSF (Price/SqFt) =====================
% Convert price from string (e.g., "RM 500,000") to numeric
transactionPrice = replace(filteredData.("Transaction Price"), "RM", "");
priceNumeric = str2double(transactionPrice);

% Calculate PSF using Land Area (converted from m² to ft²)
landArea = filteredData.("Land/Parcel Area");
filteredData.("PSF (Land/Parcel Area)") = priceNumeric./(landArea*10.7639);

% Calculate PSF using Built-Up/Main Floor Area (converted from m² to ft²)
builtUpArea = filteredData.("Main Floor Area");
filteredData.("PSF (Main Floor Area)") = priceNumeric./(builtUpArea*10.7639);

% ===================== VISUALIZATION =====================

% Boxplot: PSF by Property Type
figure;
boxplot(filteredData.("PSF (Land/Parcel Area)"),filteredData.("Property Type"));
xlabel('Property Type');
ylabel('PSF (RM)');
title('Price Per Square Foot (Land/Parcel Area) by Property Type');

% Histogram: Distribution of PSF values
figure;
valid = ~isnan(filteredData.("PSF (Land/Parcel Area)"));
histogram(filteredData.("PSF (Land/Parcel Area)")(valid), 'BinWidth', 50);
xlabel('Price Per Square Foot (Land/Parcel Area)');
ylabel('Number of Transactions');
title('Distribution of Property Prices per Square Foot');

% Scatter plot: Land area vs PSF, color-coded by Property Type
figure;
valid = ~isnan(filteredData.("Land/Parcel Area")) & ~isnan(filteredData.("PSF (Land/Parcel Area)"));
gscatter(filteredData.("Land/Parcel Area")(valid), ...
         filteredData.("PSF (Land/Parcel Area)")(valid), ...
         filteredData.("Property Type")(valid));
xlabel('Land/Parcel Area');
ylabel('Price Per Square Foot (Land/Parcel Area)');
title('Property Size vs. Price per Square Foot');
