# Project 5 — Agricultural Productivity & Yield Analysis
## Power BI Desktop modeling & DAX measures guide

This guide details the step-by-step instructions to rebuild the Capstone project dashboard natively inside Power BI Desktop using the generated clean dataset.

---

## 1. Importing & Modeling Data

1. **Load Datasets**:
   - In Power BI Desktop, click **Get Data** -> **Text/CSV**.
   - Load **`crop_production_cleaned.csv`** (contains the historical records).
   - Load **`state_zone_ref.csv`** (contains the geographic zone mapping).

2. **Establish Relationships (Model View)**:
   - Navigate to the **Model View** tab.
   - Drag a relationship from `state_zone_ref[State_Name]` (1) to `crop_production_cleaned[State_Name]` ($*$).
   - Ensure the relationship is active and the cross-filter direction is set to **Single** (Zone filters State).

---

## 2. Recreating the Normalized Yield Index

Since raw production is reported in different units (nuts for coconuts, bales for cotton, and tonnes for wheat/rice), you cannot sum raw yield across different crop types. We must normalize yields by crop type using DAX measures:

### 1. Total Area
```dax
Total Area (Ha) = SUM(crop_production_cleaned[Area])
```

### 2. Total Production
```dax
Total Production = SUM(crop_production_cleaned[Production])
```

### 3. Raw Yield
```dax
Yield Raw = DIVIDE([Total Production], [Total Area (Ha)], 0)
```

### 4. Crop Historical Mean Yield
This measure calculates the overall average yield for each crop type, ignoring any filters applied to states, zones, or years:
```dax
Crop Mean Yield = 
CALCULATE(
    AVERAGE(crop_production_cleaned[Yield]),
    ALLEXCEPT(crop_production_cleaned, crop_production_cleaned[Crop])
)
```

### 5. Normalized Yield Index
Rebases every record's yield relative to its crop's national average (1.0 = average performance for that specific crop):
```dax
Yield Index = DIVIDE([Yield Raw], [Crop Mean Yield], 0)
```

---

## 3. Visualizations Layout Guide

Structure your **Project5_Dashboard.pbix** report with three pages to mirror the design system:

### Page 1: Executive Summary
- **Title Block**: "Bharat Agricultural Diagnostics — Executive Summary"
- **KPI Cards**:
  - `Total Records` (Count of rows)
  - `States Tracked` (Distinct count of states)
  - `Crops Tracked` (Distinct count of crops)
  - `National Yield Index` (Average of `Yield_Index` for all selected records)
- **Line Chart**: National Yield Trend (Axis: `Crop_Year`, Values: `[Yield Index]`)
- **Compass Zone Visual**:
  - Use a matrix or grid structure matching the 6 zones: North, South, East, West, Northeast, and Central.
  - Apply conditional color formatting: Dark Green for index >= 1.05, Light Green for index >= 0.95, Gold for index >= 0.85, and Red for index < 0.85.

### Page 2: Detailed Analysis
- **Slicers**:
  - Year range (`Crop_Year` slider)
  - Geographic zone (`Zone` checkboxes)
  - Crop names (`Crop` dropdown list)
- **Charts**:
  - **Zone Trend**: Line chart of `[Yield Index]` over `Crop_Year` legend by `Zone`.
  - **Seasonal Share**: Donut chart showing area distribution by `Season` (Kharif, Rabi, Whole Year, etc.).
  - **Crop Area Trend**: Stacked line chart of top crops cultivated area over years.
- **Reference Tables**:
  - State rankings table: lists states, zones, records count, and average `[Yield Index]` sorted descending.

### Page 3: Recommendations
- A formatted text page summarizing the **5 Strategic Policy Recommendations** (Punjab replication, Central zone prioritization, Rajasthan/MP rainfed risk mitigation, national program support preservation, and yield-focused inputs focus).
