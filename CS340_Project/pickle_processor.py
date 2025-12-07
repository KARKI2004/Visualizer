#Version: v0.1
#Date Last Updated: 12-04-2025

'''
Version: <v0.1>
Description:
< configuration settings for file paths, figure size, and plot style>
Authors:
<Samiksha Gnawali, Suyog Karki>
Date Created : <11/30/2025>
'''


import pandas as pd
import pickle
import os

class PickleProcessor:
    def __init__(self, pickle_file):
        self.pickle_file = pickle_file
        self.data = None

    def read_pickle(self):
        try:
            with open(self.pickle_file, "rb") as f:
                self.data = pickle.load(f)
            print(f"Pickle loaded successfully. Shape: {self.data.shape}")
        except Exception as e:
            print(f"Error loading pickle: {e}")

    def show_summary(self):
        if isinstance(self.data, pd.DataFrame):
            print("\n=== Summary Statistics ===")
            print(self.data.describe())
            mean_vals = self.data.mean(numeric_only=True)
            median_vals = self.data.median(numeric_only=True)
            std_vals = self.data.std(numeric_only=True)
            summary = pd.DataFrame({"Mean": mean_vals, "Median": median_vals, "Std": std_vals})
            print("\n=== Mean / Median / Std ===")
            print(summary)
            os.makedirs("Output", exist_ok=True)
            self.data.describe().to_csv("Output/pickle_summary.csv", index=False)
            summary.to_csv("Output/pickle_mean_median_std.csv")
            print("Summary exported to Output/pickle_summary.csv")
            print("Mean/Median/Std exported to Output/pickle_mean_median_std.csv")
        else:
            print("No valid DataFrame loaded.")
