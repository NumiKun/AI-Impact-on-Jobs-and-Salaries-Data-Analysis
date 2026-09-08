# AI Impact on Jobs and Salaries: Data Analysis and Interactive Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.22%2B-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-CC0_1.0-lightgrey?style=flat-square)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Live Dashboard](https://img.shields.io/badge/Live_Demo-Streamlit_Cloud-00C04B?style=flat-square&logo=streamlit&logoColor=white)](https://ai-impact-on-jobs-and-salaries-data-analysis.streamlit.app/)

A comprehensive end-to-end data analysis and interactive web dashboard examining global compensation benchmarks, employment trajectories, and structural market shifts across artificial intelligence, machine learning, and data disciplines from 2020 through 2025.

---

## Live Interactive Dashboard

The interactive analytics platform is deployed and publicly accessible on Streamlit Community Cloud:

**[https://ai-impact-on-jobs-and-salaries-data-analysis.streamlit.app/](https://ai-impact-on-jobs-and-salaries-data-analysis.streamlit.app/)**

### Dashboard Capabilities
- **Dynamic Filtering Engine**: Multi-criteria filtering by Year (2020–2025), Experience Level, Work Mode (Remote, Hybrid, On-site), Company Size (S, M, L), Role Family, and Country.
- **Statistical Outlier Handling**: Real-time toggle to include or exclude statistical salary outliers (1.5x IQR boundary at ~$306K USD) across all calculations.
- **Interactive Visualizations**: 22 Plotly-powered charts with hover inspections, custom color palettes, and responsive layouts.
- **Modular Analysis Views**:
  - **Market Overview**: Global record growth, macro distribution, categorical breakdowns, and salary distribution modeling.
  - **Salary Analysis**: Experience-level progression curves, role family box plots, company size compensation bands, and experience-by-role heatmaps.
  - **Geographic Landscape**: Geographic hiring concentrations, median pay across top countries, and remote work ratios by country.
  - **Trends Over Time**: Multi-year compensation trajectories, year-over-year growth rates, and shifts in work-mode preferences.
  - **Role Deep Dive**: Granular head-to-head comparison across 11 standardized role families with Compound Annual Growth Rates (CAGR) and experience premiums.

---

## Key Findings and Market Insights

1. **Macro Compensation Distribution**
   - The overall compensation distribution is right-skewed with an overall median salary of **$138,000 USD** and a mean of **$146,000 USD**.
   - The middle 50% of the market (interquartile range) sits between **$95,000 USD** and **$185,000 USD**, with a specialized upper tail extending beyond $300,000 USD.

2. **The Experience Tier Multiplier**
   - Moving from **Entry-level** ($85K median) to **Mid-level** ($120K median) yields an average +41% salary increase.
   - The transition from **Mid-level** to **Senior-level** ($160K median) provides an additional +33% ($40K) premium.
   - **Executive-level** positions command a median of $210K+, demonstrating significant compensation leverage for strategic leadership roles.

3. **High-Value Role Specialization**
   - **AI Architect** and **Research Scientist** command the highest median salaries and exhibit the steepest experience gradients.
   - **Machine Learning Engineers** and **Data Engineers** represent the highest sustained job volume alongside consistent compensation growth, reflecting operational production demands.

4. **Geographic and Remote Work Patterns**
   - The United States maintains the highest absolute compensation medians, followed by specialized tech hubs in Switzerland, Israel, the United Kingdom, and Canada.
   - Hybrid and remote roles demonstrate strong compensation parity with on-site equivalents, particularly in senior and specialized engineering categories.

5. **Enterprise Hiring Structure**
   - Medium-sized organizations (100–1,000 employees) account for the vast majority of hiring volume while remaining highly competitive in compensation (within 5–8% of large corporate medians).

---

## Project Architecture

```
.
├── Analysis/
│   ├── ai_jobs_salaries_eda.ipynb    # Comprehensive exploratory data analysis notebook
│   └── figures/                      # 25 exported high-resolution analytical figures
│       ├── 00_summary_dashboard.png
│       ├── 02_salary_distribution.png
│       ├── 05_salary_trend_over_time.png
│       ├── 15_salary_heatmap_role_experience.png
│       └── ...
├── Dashboard/
│   ├── app.py                        # Streamlit interactive application source code
│   └── requirements.txt              # Application-specific dependencies
├── Dataset/
│   ├── ai_jobs_salaries_clean.csv    # Cleaned dataset (71,913 records x 17 columns)
│   └── data_dictionary.md            # Schema, column descriptions, and data provenance
├── .gitignore                        # Git exclusion rules
├── requirements.txt                  # Project-wide dependencies
└── README.md                         # Project documentation
```

---

## Dataset Overview

- **Source File**: `Dataset/ai_jobs_salaries_clean.csv`
- **Volume**: 71,913 verified records (2020 through 2025)
- **Primary Currency**: USD (`salary_in_usd`), normalized for direct cross-region comparisons
- **Key Dimensions**:
  - `work_year`: Reporting year (2020–2025)
  - `experience_level_label`: Entry-level, Mid-level, Senior-level, Executive-level
  - `employment_type_label`: Full-time, Part-time, Contract, Freelance
  - `role_family`: 11 standardized job families (e.g., AI Engineer, Data Scientist, ML Engineer)
  - `work_mode`: On-site, Hybrid, Remote
  - `company_size`: Small (S), Medium (M), Large (L)
  - `company_location`: ISO 3166-1 alpha-2 country codes
  - `salary_outlier_flag`: Boolean flag identifying records outside 1.5x IQR boundaries

For full schema details, consult the [Data Dictionary](Dataset/data_dictionary.md).

---

## Local Setup and Installation

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/NumiKun/AI-Impact-on-Jobs-and-Salaries-Data-Analysis.git
cd AI-Impact-on-Jobs-and-Salaries-Data-Analysis
```

### 2. Configure Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
# Option A: From root directory
streamlit run Dashboard/app.py

# Option B: From Dashboard directory
cd Dashboard
streamlit run app.py
```
The application will automatically open in your default browser at `http://localhost:8501`.

### 5. Run the Exploratory Data Analysis Notebook
```bash
jupyter lab Analysis/ai_jobs_salaries_eda.ipynb
# or
jupyter notebook Analysis/ai_jobs_salaries_eda.ipynb
```

---

## Technology Stack

| Component | Library / Tool | Purpose |
|---|---|---|
| Dashboard Engine | Streamlit | Web application framework and dynamic UI components |
| Interactive Visualizations | Plotly Graph Objects & Express | Interactive charts, heatmaps, box plots, and histograms |
| Data Processing | Pandas, NumPy | Data ingestion, aggregations, transformations, and pivoting |
| Statistical Analysis | SciPy Stats | Interquartile range (IQR) detection, descriptive statistics |
| Notebook Environment | Jupyter | Comprehensive exploratory data analysis workflow |
| Styling | Custom CSS / Inter Font | Enterprise light/dark sidebar theme without third-party CSS frameworks |

---

## Data Provenance and Licensing

- **Salary Dataset**: Derived and curated from [foorilla/ai-jobs-net-salaries](https://github.com/foorilla/ai-jobs-net-salaries), distributed under Creative Commons CC0 1.0 Universal Public Domain Dedication.
- **Generative AI Exposure Scoring**: Based on research by Gmyrek et al. (2025), *Global Index of Occupational Exposure to Generative AI*, International Labour Organization, licensed under CC BY 4.0.
- **Code License**: The analysis and dashboard source code are available under the MIT License.
