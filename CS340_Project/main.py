#Version: v0.1
#Date Last Updated: 11-10-2025

#%% MODULE BEGINS
module_name_gl = 'main'

'''
Version: <v0.1>
Description:
<controls the overall program flow>
Authors:
<Samiksha Gnawali, Suyog Karki>
Date Created : <11/08/2025>
Date Last Updated: <11/10/2025>
'''

#%% IMPORTS
from config import show_config
from data_handler import CSVDataProcessor
from config import CONFIG

import matplotlib.pyplot as plt
import seaborn as sns


def main():
    """Main function to execute the analysis workflow."""
    print("=== Used Car Analysis Project ===")
    show_config()

    
    csv_file = CONFIG["DATA_FILE"]
 
    processor = CSVDataProcessor(csv_file)

    
    if processor.data is not None:
        print("\n=== Basic Info ===")
        print(processor.data.info())
        print("\n=== Basic Statistics ===")
        print(processor.data.describe())

        
        print("\n=== Parent Class Plots ===")
        processor.plot_histogram('Selling_Price')
        plt.show(block=False)
        plt.pause(2)
        plt.close()

        processor.plot_line('Year', 'Selling_Price')
        plt.show(block=False)
        plt.pause(2)
        plt.close()

       
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

        
        print("\n=== Simple Query ===")
        result_simple = processor.query_simple('Owner', 0)
        print(result_simple.head())

        print("\n=== Boolean Query ===")
        conditions = {'Fuel_Type': 'Petrol', 'Owner': 0}
        result_boolean = processor.query_boolean(conditions)
        print(result_boolean.head())
        plt.close()


if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    main()
