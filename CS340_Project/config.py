from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"
DOC_DIR = BASE_DIR / "Doc"

# Input files
CSV_FILE = INPUT_DIR / "car data.csv"  # Note: includes space in name
PKL_FILE = INPUT_DIR / "car data.pkl"
