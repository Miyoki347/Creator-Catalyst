import pandas as pd
import sys

try:
    df = pd.read_csv('test_data.csv')
    print(f"Columns: {df.columns.tolist()}")
except Exception as e:
    print(f"Error: {e}")
