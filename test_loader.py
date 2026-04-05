from data_loader import loader
import pandas as pd

def test():
    file_path = 'test_data.csv'
    result = loader.load_csv(file_path)
    df = result['data']
    has_date = result['has_date']
    
    print(f"Data Loaded: {has_date}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Rows after cleaning: {len(df)}")
    
    # Check for '合計'
    if df.astype(str).apply(lambda row: row.str.contains('合計|Total', case=False).any(), axis=1).any():
        print("FAILED: '合計' row remains!")
    else:
        print("SUCCESS: '合計' row removed.")
        
    # Check for formatting of 'metric' (viewer counts with commas)
    if (df['metric'] > 1000).any():
        print("SUCCESS: Numeric values with commas were correctly parsed.")
    else:
        print("FAILED: Numeric values with commas missed!")

    # Explicitly check time conversion if it was mapped as 'metric'
    # Actually, metric in test_data.csv is 'ビュー数' (views). 
    # Let's test time conversion specifically.
    time_str = "0:02:06"
    secs = loader.convert_duration_to_seconds(time_str)
    print(f"Time conversion '{time_str}' -> {secs} seconds.")
    if secs == 126.0:
        print("SUCCESS: Duration format '0:02:06' correctly converted.")
    else:
        print(f"FAILED: Duration format conversion incorrect ({secs}).")

if __name__ == "__main__":
    test()
