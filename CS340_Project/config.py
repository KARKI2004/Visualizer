# config.py

# Configuration constants
CONFIG = {
    "BASE_DIR": r"c:\Users\samik\CMPS_3400_Project\CS340_Project",
    "DATA_FILE": r"c:\Users\samik\CMPS_3400_Project\CS340_Project\Input\car_data.csv",
    "PLOT_STYLE": "darkgrid",
    "FIG_SIZE": (10, 6),
    "TARGET_COLUMN": "Selling_Price"
}


def show_config():
    """Print the configuration settings."""
    print("=== Configuration Settings ===")
    for key, value in CONFIG.items():
        print(f"{key}: {value}")

# Set plot style globally
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style(CONFIG["PLOT_STYLE"])  # must be: white, dark, whitegrid, darkgrid, ticks
plt.rcParams["figure.figsize"] = CONFIG["FIG_SIZE"]
