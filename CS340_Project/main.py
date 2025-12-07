# Version: v0.3
# Date Last Updated: 12-04-2025

'''
Version: <v0.3>
Description:
<Main controller that executes data handling, visualization, and analytics modules>
Authors:
<Samiksha Gnawali, Suyog Karki>
Date Created : <11/08/2025>
'''

module_name_gl = 'main'

from config import show_config, CONFIG
from data_handler import CSVDataProcessor
from analytics import ProbabilityAnalyzer
import matplotlib.pyplot as plt


def main():
    print(f"\"{module_name_gl}\" module begins.")
    print("=== Used Car Analysis Project ===")
    show_config()

    csv_file = CONFIG["DATA_FILE"].replace(".pkl", ".csv")
    processor = CSVDataProcessor(csv_file)

    if processor.data is not None:
        print("\n=== Basic Info ===")
        print(processor.data.info())
        print("\n=== Basic Statistics ===")
        print(processor.data.describe())

        print("\n=== Parent Class Plots ===")
        processor.plot_histogram('Selling_Price')
        processor.plot_line('Year', 'Selling_Price')

        print("\n=== Child Class Plots ===")
        processor.plot_violin('Selling_Price')
        processor.plot_box('Present_Price')
        processor.plot_scatter('Kms_Driven', 'Selling_Price')

        print("\n=== Simple Query ===")
        result_simple = processor.query_simple('Owner', 0)
        print(result_simple.head())

        print("\n=== Boolean Query ===")
        conditions = {'Fuel_Type': 'Petrol', 'Owner': 0}
        result_boolean = processor.query_boolean(conditions)
        print(result_boolean.head())

    # === PART 2: ANALYTICS (PICKLE DATA, VECTOR + PROBABILITY) ===
    print("\n=== Probability & Vector Analysis ===")
    pickle_file = CONFIG["DATA_FILE"]
    analyzer = ProbabilityAnalyzer(pickle_file)
    analyzer.read_pickle()
    analyzer.show_summary()

    # Probability computations
    analyzer.joint_counts("Fuel_Type", "Transmission")
    analyzer.joint_probability("Fuel_Type", "Transmission")
    analyzer.conditional_probability("Fuel_Type", "Seller_Type")

    # Vector operations
    vec_a = analyzer.data["Selling_Price"].values[:5]
    vec_b = analyzer.data["Present_Price"].values[:5]
    analyzer.vector_operations(vec_a, vec_b)

    # Categorical analysis
    analyzer.categorical_analysis("Fuel_Type")

    print("\nAll outputs generated in Output/ folder!")


if __name__ == "__main__":
    main()
