import pandas as pd
from pathlib import Path
from datetime import datetime
import os

# setup paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

def get_latest_file(directory):
    """
    Finds the most recently created CSV file in the specified directory.
    Simulates picking up the latest daily data dump.
    """
    files = list(directory.glob('*.csv'))
    
    if not files:
        raise FileNotFoundError(f"No CSV files found in {directory}. Run ingestion first")
    
    # sort by modification time and grab the newest one
    latest_file = max(files, key=os.path.getmtime)
    print(f"--> Found latest file: {latest_file.name}")
    return latest_file

def transform_data(file_path):
    """
    Applies logic to clean and standardize the dataset.
    """
    print("--> Starting transformation...")
    df = pd.read_csv(file_path)
    
    # handle missing data
    # mock business rule: If location is missing, assume 'Remote'
    if 'office_location' in df.columns:
        missing_count = df['office_location'].isnull().sum()
        if missing_count > 0:
            print(f"    - Filling {missing_count} missing office locations with 'Remote'")
            df['office_location'] = df['office_location'].fillna('Remote')
    
    # type conversion
    # CSVs load dates as strings, so convert to datetime
    print("    - Converting 'hire_date' to datetime objects")
    df['hire_date'] = pd.to_datetime(df['hire_date'])
    
    # feaure engineering: adding a tenure field
    today = pd.Timestamp.now()
    df['tenure_years'] = ((today - df['hire_date']).dt.days / 365.25).round(1)
    
    return df

def save_to_parquet(df, filename_prefix):
    """
    Saves the clean data to the processed folder in Parquet format.
    """
    # ensure the folder exists
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = PROCESSED_DIR / f"{filename_prefix}_{timestamp}.parquet"
    
    # save as parquet
    df.to_parquet(str(file_path), index=False)
    print(f"SUCCESS: Processed data saved to {file_path}")

# execute the flow
if __name__ == "__main__":
    try:
        # find the raw data
        latest_file = get_latest_file(RAW_DIR)
        
        # clean the data
        clean_df = transform_data(latest_file)
        
        # save the data
        save_to_parquet(clean_df, "employees_clean")
        
    except Exception as e:
        print(f"❌ PIPELINE FAILED: {e}")