# main.py

#%% MODULE BEGINS
module_name_gl = 'main'

'''
Version: v1.0
Description:
Main driver script for the Used Car Analysis project.
Uses parent and child classes to visualize and query data.

Authors:
Your Name
Date Created : 11-08-2025
Date Last Updated: 11-08-2025
'''

#%% IMPORTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from config import show_config

from data_handler import CSVDataProcessor

import matplotlib.pyplot as plt
import seaborn as sns

#%% FUNCTION DEFINITIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    """Main function to execute the analysis workflow."""
    print("=== Used Car Analysis Project ===")
    show_config()

    # --- Initialize Child class with CSV ---
    from config import CONFIG
    csv_file = CONFIG["DATA_FILE"]
  # Update with correct path
    processor = CSVDataProcessor(csv_file)

    # --- Basic info and statistics ---
    if processor.data is not None:
        print("\n=== Basic Info ===")
        print(processor.data.info())
        print("\n=== Basic Statistics ===")
        print(processor.data.describe())

        # --- Parent class visualizations ---
        print("\n=== Parent Class Plots ===")
        processor.plot_histogram('Selling_Price')
        plt.show(block=False)
        plt.pause(2)
        plt.close()

        processor.plot_line('Year', 'Selling_Price')
        plt.show(block=False)
        plt.pause(2)
        plt.close()

        # --- Child class advanced visualizations ---
        print("\n=== Child Class Plots ===")
        processor.plot_violin('Selling_Price')
        plt.show(block=False)
        plt.pause(2)
        plt.close()

        processor.plot_box('Present_Price')
        plt.show(block=False)
        plt.pause(2)
        plt.close()

        processor.plot_scatter('Kms_Driven', 'Selling_Price')
        plt.show(block=False)
        plt.pause(2)
        plt.close()

        # --- Queries ---
        print("\n=== Simple Query ===")
        result_simple = processor.query_simple('Owner', 0)
        print(result_simple.head())

        print("\n=== Boolean Query ===")
        conditions = {'Fuel_Type': 'Petrol', 'Owner': 0}
        result_boolean = processor.query_boolean(conditions)
        print(result_boolean.head())
        plt.close()

#%% SELF-RUN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    main()
