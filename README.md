# 🌾 Agricultural Productivity & Yield Analysis in India

### End-to-End Analytics Pipeline (Excel + Python + SQL + Power BI)

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 About the Project

India is one of the world's largest agricultural economies, yet productivity varies dramatically across states, zones, and crop types. Traditional reporting relies on raw production figures — but these are fundamentally **incomparable across crops** (sugarcane is measured in tonnes, coconut in nuts).

This project builds a **complete analytics pipeline** that solves this problem using a **Normalized Yield Index** — a metric that rebases every record's yield relative to its crop's national average (1.0 = national average), enabling meaningful cross-crop and cross-region comparisons.

> **Capstone Project** — LinuxWorld Informatics Pvt. Ltd. Summer Industrial Training 2026

---

## 🏗️ Pipeline Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  📊 Excel    │ ──→ │  🐍 Python   │ ──→ │  🗄️ SQL      │ ──→ │  📈 Power BI │
│  CSV Data    │     │  EDA + Stats │     │  SQLite DB   │     │  Dashboard   │
│  Preparation │     │  Analysis    │     │  Queries     │     │  3 Pages     │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

---

## 📂 Repository Structure

```
Project5_Crop_Analytics/
│
├── 📓 Project5_Pipeline.ipynb        # Main pipeline notebook (data gen → SQL → analysis)
├── 📓 Project5_EDA.ipynb             # Exploratory Data Analysis & statistical modeling
├── 📝 Project5_Queries.sql           # 6 SQL tasks (aggregations, JOINs, CTEs, window functions)
├── 📊 Project5_Dashboard.pbix        # Power BI interactive dashboard (3 pages)
├── 📄 Project5_Dashboard_Pages.pdf   # Dashboard screenshots (PDF export)
├── 📖 Project5_Power_BI_Build_Guide.md  # Step-by-step Power BI recreation guide
├── 📑 Project5_Report.html           # Professional project report (open in browser → print as PDF)
│
├── 🐍 generate_dataset.py            # Automated dataset generator script
├── 📊 crop_production_cleaned.csv     # Cleaned dataset (10,000+ records)
├── 📊 state_zone_ref.csv             # State-to-Zone geographic mapping
├── 🗄️ crop_production.db             # SQLite database file
│
└── 📄 README.md                      # This file
```

---

## 🔍 Key Findings

| Zone | Records | Avg Yield Index | Performance |
|------|---------|-----------------|-------------|
| South | 2,215 | 1.0815 | ✅ Above Average |
| North | 1,845 | 1.0257 | ✅ Above Average |
| West | 1,540 | 1.0131 | ✅ Above Average |
| East | 1,558 | 0.9461 | ⚠️ Below Average |
| Northeast | 2,141 | 0.9345 | ⚠️ Below Average |
| Central | 578 | 0.7261 | 🔴 Critical |

### Critical Insights
- 📉 **Farm Size ≠ Productivity** — Correlation between area and yield index is near zero (r = -0.01)
- 🔴 **Central Zone Crisis** — Operates at only 72.6% of national average yield
- 🌱 **Seasonal Dynamics** — Kharif dominates area, but Rabi shows more consistent yields
- 🏆 **South Zone Leadership** — Consistently outperforms at 1.08 Yield Index

---

## 🛠️ Technologies Used

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Data Prep | Excel / CSV | Raw data cleaning and interchange format |
| Analysis | Python (Pandas, NumPy, Matplotlib, Seaborn) | EDA, statistical modeling, visualization |
| Database | SQLite / SQLite3 | JOINs, CTEs, Window Functions, VIEWs |
| BI Dashboard | Power BI Desktop (DAX) | Interactive 3-page dashboard with KPIs |

---

## 📊 SQL Analysis Overview

Six structured SQL tasks demonstrate progressive complexity:

| Task | Concept | Description |
|------|---------|-------------|
| 1 | Aggregations | SUM, AVG, MIN, MAX by crop type |
| 2 | Filtering | Year range + outlier exclusion |
| 3 | INNER JOIN | Crop records + zone mapping |
| 4 | Window Functions | RANK by zone, LAG for YoY growth |
| 5 | CTEs | Districts performing 25%+ above state average |
| 6 | VIEWs | Denormalized view for BI consumption |

---

## 📈 Power BI Dashboard

The dashboard consists of 3 interactive pages:

1. **Executive Summary** — KPI cards, national yield trend, zone performance compass
2. **Detailed Analysis** — Slicers (year, zone, crop), trend charts, seasonal breakdown
3. **Recommendations** — 5 strategic policy recommendations

> 📄 See [Project5_Dashboard_Pages.pdf](Project5_Dashboard_Pages.pdf) for dashboard screenshots

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook
- Power BI Desktop (for `.pbix` file)

### Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Agricultural-Productivity-Analysis-India.git
cd Agricultural-Productivity-Analysis-India

# Install Python dependencies
pip install pandas numpy matplotlib seaborn

# Run the pipeline notebook
jupyter notebook Project5_Pipeline.ipynb
```

---

## 💡 5 Strategic Recommendations

1. **Replicate Punjab's success** in underperforming northern states
2. **Prioritize Central zone** (MP, Chhattisgarh) for targeted investment
3. **Build rainfed risk mitigation** for Rajasthan & MP
4. **Preserve national programs** that are already delivering results
5. **Shift to yield-focused inputs** (seeds, fertilizers, irrigation) over area expansion

---

## 👤 Author

**Trivedi Dharmik.H.**
- 🎓 B.Tech CSE — ITM SLS Baroda University
- 📧 dharmiktrivedi595@gmail.com
- 🏢 Summer Industrial Training — LinuxWorld Informatics Pvt. Ltd.

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **LinuxWorld Informatics Pvt. Ltd.** — For mentorship and training guidance
- **Ministry of Agriculture & Farmers Welfare, GOI** — For agricultural statistics via [data.gov.in](https://data.gov.in)
