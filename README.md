# HR Data Engineering Pipeline

## Project Overview
This project demonstrates a full **Extract, Transform, Load (ETL)** pipeline designed to handle high-volume employee data. 

The goal was to migrate away from manual Excel/CSV workflows into an automated, version-controlled engineering pipeline. It simulates a real-world scenario where raw data is ingested from an upstream source (simulated via Python), cleaned/validated using Pandas, and optimized for analytical querying using **Parquet** and **DuckDB**.

## Architecture
**`Raw CSV`** → **`Python Ingestion`** → **`Pandas Transformation`** → **`Parquet Storage`** → **`DuckDB Analytics`**

### Key Engineering Decisions
* **Idempotency:** The pipeline is designed to be run multiple times without corrupting data. File paths are dynamically generated using timestamps to preserve history (Slowly Changing Dimensions Type 0 concept).
* **Schema Enforcement:** Switched from CSV to **Parquet** in the processed layer. This ensures data types (like Dates and Floats) are preserved, reducing storage size by ~60% and improving query speed.
* **Decoupled Compute/Storage:** Utilized **DuckDB** to run SQL queries directly on Parquet files, eliminating the need for a heavy Data Warehouse for lightweight analytics.
* **Defensive Coding:** Implemented relative path handling (`pathlib`) to ensure the pipeline runs seamlessly across Windows and Linux environments.

## Tech Stack
* **Language:** Python 3.9+
* **Libraries:** Pandas, Faker, Pathlib
* **Storage:** Parquet (Columnar), CSV (Raw)
* **Analytics:** DuckDB, Jupyter Notebooks, SQL

## Repository Structure
```text
├── data/
│   ├── raw/             # Generated mock data (simulating S3 bucket)
│   ├── processed/       # Cleaned Parquet files
├── notebooks/           # Jupyter notebooks for SQL analysis
├── src/
│   ├── ingestion/       # Scripts to generate/fetch data
│   ├── transform/       # Logic for cleaning and schema enforcement
├── requirements.txt     # Python dependencies
└── README.
```

How to Run
```bash
1. Clone the repository
git clone <your-repo-url>
```
```bash
2. Install Dependencies
pip install -r requirements.txt
```
```bash
3. Run the Pipeline
# Step 1: Generate Raw Data
python src/ingestion/generate_data.py

# Step 2: Clean and Transform
python src/transform/clean_data.py
```

4. Run and view queries on the data ```bash
notebooks/analysis.ipynb```