# Legacy CLI pipeline for class project.
# Streamlit app uses app.py and st.file_uploader instead.

module_name_gl = 'main'

from src.config import show_config, CONFIG
from src.data_handler import CSVDataProcessor
from src.analytics import ProbabilityAnalyzer
from src.pickle_processor import PickleProcessor
from src.module_tmp import (
    DEFAULT_SHAPE,
    make_numpy_dataframe,
    export_dataframe_pickle,
    safe_eval,
    apply_transformations,
    summarize_with_kwargs,
    make_counter,
    TempCache,
)
import matplotlib.pyplot as plt
import os


def main():
    print(f"\"{module_name_gl}\" module begins.")
    print("=== Used Car Analysis Project ===")
    show_config()

    os.makedirs("Output", exist_ok=True)

    csv_file = CONFIG["DATA_FILE"].replace(".pkl", ".csv")
    processor = CSVDataProcessor(csv_file)

    if processor.data is not None:
        processor.log("CSV data loaded successfully.")
        print("\n=== Basic Info ===")
        print(processor.data.info())
        print("\n=== Basic Statistics ===")
        print(processor.data.describe())

        print("\n=== Parent Class Plots ===")
        try:
            processor.plot_histogram(
                'Selling_Price',
                show=False,
                save_path="Output/histogram_Selling_Price.png"
            )
            processor.plot_line(
                'Year',
                'Selling_Price',
                show=False,
                save_path="Output/line_Year_Selling_Price.png"
            )
        except Exception as exc:
            processor.log(f"Plot error (parent plots): {exc}")

        print("\n=== Child Class Plots ===")
        try:
            processor.plot_violin(
                'Selling_Price',
                show=False,
                save_path="Output/violin_Selling_Price.png"
            )
            processor.plot_box(
                'Present_Price',
                show=False,
                save_path="Output/box_Present_Price.png"
            )
            processor.plot_scatter(
                'Kms_Driven',
                'Selling_Price',
                show=False,
                save_path="Output/scatter_Kms_Driven_Selling_Price.png"
            )
        except Exception as exc:
            processor.log(f"Plot error (child plots): {exc}")

        print("\n=== Simple Query ===")
        result_simple = processor.query_simple('Owner', 0)
        print(result_simple.head())

        print("\n=== Boolean Query ===")
        conditions = {'Fuel_Type': 'Petrol', 'Owner': 0}
        result_boolean = processor.query_boolean(conditions)
        print(result_boolean.head())

        # Boolean indexing example
        try:
            mask = (processor.data["Owner"] == 0) & (processor.data["Fuel_Type"] == "Petrol")
            print("\n=== Boolean Indexing Example ===")
            print(processor.data[mask].head())
        except Exception as exc:
            processor.log(f"Boolean indexing error: {exc}")

        # *args / **kwargs, lambda, eval, nonlocal, and private-like variable usage
        print("\n=== module_tmp Features ===")
        tmp_rows, tmp_cols = DEFAULT_SHAPE
        numpy_df = make_numpy_dataframe(tmp_rows, tmp_cols)
        numpy_df.to_csv("Output/numpy_df.csv", index=False)
        export_dataframe_pickle(numpy_df, "Output/numpy_df.pkl")
        summary_all = summarize_with_kwargs(numpy_df, include="all")
        print(summary_all)

        eval_result = safe_eval("a + b * 2", a=2, b=3)
        print(f"Eval result: {eval_result}")

        transformed = apply_transformations([1, 2, 3], lambda x: x * 2, lambda x: x + 1)
        print(f"Transformed values: {transformed}")

        counter = make_counter()
        print(f"Nonlocal counter: {counter()}, {counter()}")

        cache = TempCache()
        cache.set("status", "ok")
        print(f"Private-like cache value: {cache.get('status')}")
        processor.log("Completed CSV analysis steps.")

    # === PART 2: ANALYTICS (PICKLE DATA, VECTOR + PROBABILITY) ===
    print("\n=== Probability & Vector Analysis ===")
    pickle_file = CONFIG["DATA_FILE"]
    analyzer = ProbabilityAnalyzer(pickle_file)
    analyzer.read_pickle()
    analyzer.show_summary()

    # Mean / Median / Std from pickle data
    pickle_processor = PickleProcessor(pickle_file)
    pickle_processor.read_pickle()
    pickle_processor.show_summary()

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

    processor.log("Completed pickle analysis steps.")
    print("\nAll outputs generated in Output/ folder!")


if __name__ == "__main__":
    main()


