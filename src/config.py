import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = Path(__file__).resolve().parent

CONFIG = {
    "APP_ROOT": str(APP_ROOT),
    "BASE_DIR": str(BASE_DIR),
    "DATA_FILE": str(APP_ROOT / "data" / "demo" / "car_data.pkl"),
    "PLOT_STYLE": "darkgrid",
    "FIG_SIZE": (10, 6),
    "TARGET_COLUMN": "Selling_Price",
}


def show_config():
    """Print the configuration settings."""
    print("=== Configuration Settings ===")
    for key, value in CONFIG.items():
        print(f"{key}: {value}")


sns.set_style(CONFIG["PLOT_STYLE"])
plt.rcParams["figure.figsize"] = CONFIG["FIG_SIZE"]

