import pandas as pd
from config import CSV_FILE

def main():
    try:
        df = pd.read_csv(CSV_FILE)
        print("✅ CSV loaded successfully!")
        print(df.head())
    except FileNotFoundError:
        print("⚠️ CSV file not found. Please place 'car data.csv' in the Input folder.")

if __name__ == "__main__":
    main()
