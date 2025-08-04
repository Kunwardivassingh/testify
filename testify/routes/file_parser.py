import pandas as pd
from extensions import db
from models.test_data import TestData  # Placeholder model

def parse_file(file_content, filename):
    if filename.endswith('.csv'):
        df = pd.read_csv(file_content)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(file_content)
    else:
        raise ValueError("Unsupported file format")
    
    for _, row in df.iterrows():
        test_data = TestData(**row.to_dict())
        db.session.add(test_data)
    db.session.commit()
    return df