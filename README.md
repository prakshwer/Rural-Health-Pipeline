# 🏥 Rural Health Intelligence Pipeline

> A complete end-to-end data engineering pipeline for rural community healthcare monitoring, disease outbreak detection, and health worker performance tracking.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![dbt](https://img.shields.io/badge/dbt-1.11-orange?style=for-the-badge&logo=dbt)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red?style=for-the-badge&logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge)

---

## 🌐 Live Demo

**[👉 Click here to open the live app](https://rural-health-pipeline-b7tpkhxc3zuqfqkgxp6grm.streamlit.app/)**

> Type any village name, generate patient data, upload a CSV, or connect a Google Sheet — and see live disease outbreak alerts and health worker performance metrics instantly.

---

## 📌 What Problem Does This Solve?

In rural India, healthcare managers face a critical challenge:

- Health workers visit **hundreds of patients** across **dozens of villages** every day
- All data is scattered in **paper registers and Excel files**
- No one can see **which village has a disease outbreak forming**
- No one can track **which health worker is underperforming**
- Vulnerable groups like **children under 5 and elderly** get missed

This pipeline solves all of that — ingesting raw patient visit data, transforming it with dbt, and surfacing **real-time outbreak alerts and performance metrics** on a live dashboard.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                            │
│  CSV Upload  │  Google Sheets  │  Synthetic Data Generator  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  INGESTION LAYER                            │
│         Python + Pydantic Validation                        │
│   Validates age, temperature, gender, required fields       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   STORAGE LAYER                             │
│              SQLite Data Warehouse                          │
│                raw_patients table                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                TRANSFORMATION LAYER (dbt)                   │
│  stg_patients → fct_village_health                          │
│              → fct_worker_performance                       │
│              → fct_disease_trends                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  SERVING LAYER                              │
│            Streamlit Dashboard                              │
│  Outbreak Alerts │ Worker Performance │ Disease Trends      │
│  Village Health  │ Vulnerable Groups                        │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🚨 Disease Outbreak Surveillance
- Real-time alerts when disease cases spike in a village
- Three alert levels — OUTBREAK ALERT, WATCH, NORMAL
- Treemap visualization of disease spread across villages

### 👩‍⚕️ Health Worker Performance Tracker
- Total visits, villages covered, diseases handled per worker
- Referral rate analysis
- Child and elderly visit tracking

### 🏘️ Village Health Summary
- Village-by-village health score
- Fever rate, referral rate, patient demographics
- Side-by-side village comparison

### 📊 Disease Trends Over Time
- Monthly disease trend lines
- Disease distribution pie chart
- Cases by disease and month

### 👶 Vulnerable Population Tracker
- Children under 5 monitoring
- Elderly patients (60+) tracking
- High risk disease case mapping
- Age group sunburst chart

---

## 🗂️ Project Structure

```
rural-health-pipeline/
│
├── ingestion/
│   ├── __init__.py
│   ├── generate_data.py        # Synthetic patient data generator
│   ├── validate_load.py        # Pydantic validation + SQLite loader
│   └── google_sheets.py        # Google Sheets connector
│
├── health_dbt/
│   ├── models/
│   │   ├── sources.yml
│   │   ├── schema.yml
│   │   ├── staging/
│   │   │   └── stg_patients.sql      # Clean + validate raw data
│   │   └── marts/
│   │       ├── fct_village_health.sql     # Village health summary
│   │       ├── fct_worker_performance.sql # Worker metrics
│   │       └── fct_disease_trends.sql     # Disease trend analysis
│   └── dbt_project.yml
│
├── app/
│   └── dashboard.py            # Streamlit dashboard
│
├── data/
│   └── raw/                    # Raw JSON backup files
│
├── sample_template.csv         # CSV template for data upload
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.11+
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/rural-health-pipeline.git
cd rural-health-pipeline
```

### Step 2 — Create virtual environment
```bash
# Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Generate sample data
```bash
python -m ingestion.validate_load
```

### Step 5 — Run dbt transformations
```bash
cd health_dbt
dbt run
dbt test
cd ..
```

### Step 6 — Launch dashboard
```bash
streamlit run app/dashboard.py
```

Open `http://localhost:8501` in your browser.

---

## 📥 How to Add Your Own Data

### Way 1 — Upload CSV File
1. Download `sample_template.csv` from this repo
2. Fill in your patient records
3. Open the app → sidebar → **Upload CSV File**
4. Upload your file and click **Load into Database**

### Way 2 — Connect Google Sheets
1. Open your Google Sheet
2. Click **Share** → **Anyone with link** → **Viewer**
3. Copy the link
4. Open the app → sidebar → **Google Sheets**
5. Paste the link and click **Fetch from Google Sheets**

Your sheet must have these columns:
```
patient_id, name, age, gender, village, visit_date, diagnosis,
temperature_c, systolic_bp, diastolic_bp, blood_glucose,
referred_to_hospital, health_worker_id, health_worker_name
```

### Way 3 — Generate Test Data
Open the app → sidebar → **Generate Fake Data** → click **Generate + Load Data**

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core programming language |
| Pydantic | Data validation and schema enforcement |
| pandas | Data manipulation and transformation |
| SQLAlchemy | Database ORM and connection management |
| SQLite | Lightweight data warehouse |
| dbt | SQL transformation framework |
| Streamlit | Interactive dashboard and UI |
| Plotly | Charts and visualizations |
| Faker | Synthetic data generation |
| Git + GitHub | Version control |
| Streamlit Cloud | Free cloud deployment |

---

## 🧪 dbt Models

| Model | Type | Description |
|-------|------|-------------|
| `stg_patients` | Staging | Cleans raw data, adds fever status, BP status, age groups |
| `fct_village_health` | Mart | Village-level health summary with outbreak detection |
| `fct_worker_performance` | Mart | Per health worker visit and performance metrics |
| `fct_disease_trends` | Mart | Monthly disease trend analysis per village |

### Run dbt tests
```bash
cd health_dbt
dbt test
```
All 8 data quality tests should pass ✅

---

## 🔒 Data Privacy

- No real patient data is used in this project
- All data is synthetically generated using Python's Faker library
- This is standard practice in data engineering for building and testing pipelines
- In production, all patient data would be encrypted and access-controlled
- API keys and credentials are stored in environment variables, never hardcoded

---

## 🎯 Skills Demonstrated

- ✅ End-to-end ELT pipeline design
- ✅ API and third-party data ingestion
- ✅ Data validation with Pydantic
- ✅ SQL and database management
- ✅ dbt transformation framework
- ✅ Data quality testing
- ✅ Interactive dashboard development
- ✅ Cloud deployment
- ✅ Data privacy awareness
- ✅ Version control with Git

---

## 👤 Author

**Prakshwer** — Data Engineering Portfolio Project

[![GitHub](https://img.shields.io/badge/GitHub-prakshwer-black?style=flat&logo=github)](https://github.com/prakshwer)

---

> Built as a portfolio project demonstrating real-world data engineering skills for rural healthcare use cases.
