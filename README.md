# PropertyAnalysis MATLAB and Python

# Property Transaction Data Analysis (Malaysia)

This MATLAB script processes and analyzes Malaysian property transaction data based on user-defined filters such as state, property type, year, and more. It visualizes pricing trends by calculating price per square foot (PSF) and provides insights using various plots.

---

## Dataset

The data is sourced from the **National Property Information Centre (NAPIC)**. You can download the **Open Sales Data (Transaction Data)** CSV from the official portal:

https://napic2.jpph.gov.my/en/open-sales-data?category=36&id=241

The script uses a CSV file named:

    Open Transaction Data.csv

Make sure this file is located in the same directory as the script. The dataset should include fields such as:

- Transaction Price
- Land/Parcel Area
- Main Floor Area
- District
- Property Type
- Tenure
- Month, Year of Transaction Date

---

## User Inputs

You can customize the analysis by modifying the following variables in the script:

```matlab
interestedSector         % e.g., "Residential", "Commercial", "Industrial"
interestedState          % e.g., ["Kuala Lumpur"]
interestedDistrict       % e.g., ["Petaling"]
interestedPropertyType   % e.g., ["Condominium/Apartment", "Service Apartment"]
interestedYear           % e.g., ["2023", "2024"]
interestedTenure         % e.g., ["Freehold", "Leasehold"]
````

Leave a variable as an empty array `[]` to ignore that filter.

---

## Features

### Filtering:

* Filter transaction data by:

  * State
  * District
  * Sector
  * Property Type
  * Year
  * Tenure

### Calculations:

* Computes **Price per Square Foot (PSF)** based on:

  * Land/Parcel Area
  * Main Floor Area

### Visualizations:

* **Boxplot** of PSF by property type
* **Histogram** of PSF distribution
* **Scatter plot** of land area vs PSF (color-coded by property type)

---

## Outputs

The script generates the following plots:

1. **Boxplot**: PSF (Land Area) vs Property Type
2. **Histogram**: Distribution of PSF values
3. **Scatter Plot**: Land Area vs PSF (colored by property type)

These plots help in comparing property values and understanding pricing trends across different types and regions.

---

## Notes

* **Area Conversion**: The script converts areas from square meters to square feet using:
  1 m² = 10.7639 ft²

* **Price Parsing**: The price strings (e.g., "RM 500,000") are cleaned and converted to numerical values for calculations.

* **Data Dictionaries**: The script includes mappings of:

  * States to their respective districts
  * Sectors to relevant property types

---

## Requirements

* MATLAB (recommended R2020b or newer)
* A properly formatted `Open Transaction Data.csv` file

---

## Author

This script was written to analyze Malaysian property transaction data for market trends and comparative valuation.

---

## Example Usage

To analyze only "Condominium/Apartment" transactions in Kuala Lumpur for the year 2024:

```matlab
interestedState = ["Kuala Lumpur"];
interestedPropertyType = ["Condominium/Apartment"];
interestedYear = ["2024"];
```

---

## License

This project is open for educational and non-commercial use. If you build upon it, credit is appreciated.

```

---

Let me know if you'd like me to include additional sections like a sample plot preview, data schema, or command-line usage.
```
