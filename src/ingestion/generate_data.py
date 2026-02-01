import pandas as pd
from faker import Faker
import random
from datetime import datetime
from pathlib import Path

# setup
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
            # add dirty data to clean later
            'office_location': random.choice(['New York', 'London', 'Remote', None]) 
        }
        data.append(record)
    
    return data

def save_to_csv(data, filename):
    """
    Saves the data to a CSV file in the raw folder.
    Uses pathlib for cross-platform compatibility.
    """
    # find the project root
    project_root = Path(__file__).resolve().parent.parent.parent
    
    # define target path
    raw_dir = project_root / "data" / "raw"
    
    # ensure directory exists
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # generate filename with timestamp 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{filename}_{timestamp}.csv"
    file_path = raw_dir / full_filename
    
    # save
    try:
        df = pd.DataFrame(data)
        df.to_csv(str(file_path), index=False)
        print(f"SUCCESS: Data generated and saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    # simulate fetching 500 records from an upstream HR system
    employee_data = generate_employee_data(500)
    save_to_csv(employee_data, "employees_raw")