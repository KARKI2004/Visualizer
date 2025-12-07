#Version: v0.1
#Date Last Updated: 12-04-2025

'''
Version: <v0.1>
Description:
< configuration settings for file paths, figure size, and plot style>
Authors:
<Samiksha Gnawali, Suyog Karki>
Date Created : <11/08/2025>
Date Last Updated: <11/10/2025>
'''

#%% IMPORTS
import matplotlib.pyplot as plt
import seaborn as sns

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    "BASE_DIR": BASE_DIR,
    "DATA_FILE": os.path.join(BASE_DIR, "Input", "car_data.pkl"),
    "PLOT_STYLE": "darkgrid",
    "FIG_SIZE": (10, 6),
    "TARGET_COLUMN": "Selling_Price"
}


def show_config():
    """Print the configuration settings."""
    print("=== Configuration Settings ===")
    for key, value in CONFIG.items():
        print(f"{key}: {value}")


sns.set_style(CONFIG["PLOT_STYLE"])  
plt.rcParams["figure.figsize"] = CONFIG["FIG_SIZE"]
