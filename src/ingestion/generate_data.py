import pandas as pd
from faker import Faker
import random
from datetime import datetime
from pathlib import Path

# 1. Setup
fake = Faker()

def generate_employee_data(num_records=100):
    """
    Generates a list of dictionaries containing mock employee data.
    """
    print(f"Generating {num_records} employee records...")
    
    data = []
    departments = ['Engineering', 'Sales', 'HR', 'Marketing', 'Product']
    
    for _ in range(num_records):
        record = {
            'employee_id': fake.uuid4(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'hire_date': fake.date_between(start_date='-5y', end_date='today'),
            'department': random.choice(departments),
            'salary': round(random.uniform(50000, 150000), 2),
            # Introduce some "dirty" data for us to clean later
            'office_location': random.choice(['New York', 'London', 'Remote', None]) 
        }
        data.append(record)
    
    return data

def save_to_csv(data, filename):
    """
    Saves the data to a CSV file in the raw folder.
    Uses pathlib for cross-platform compatibility.
    """
    # 1. Find the project root dynamically
    # (Go up 2 levels from src/ingestion)
    project_root = Path(__file__).resolve().parent.parent.parent
    
    # 2. Define target path
    raw_dir = project_root / "data" / "raw"
    
    # 3. Ensure directory exists
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # 4. Generate filename with timestamp (Idempotency)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{filename}_{timestamp}.csv"
    file_path = raw_dir / full_filename
    
    # 5. Save (Convert path to string for Pandas compatibility)
    try:
        df = pd.DataFrame(data)
        df.to_csv(str(file_path), index=False)
        print(f"SUCCESS: Data generated and saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    # Simulate fetching 500 records from an upstream HR system
    employee_data = generate_employee_data(500)
    save_to_csv(employee_data, "employees_raw")