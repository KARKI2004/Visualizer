# data_handler.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===== Parent Class =====
class DataVisualizer:
    """
    Parent class to store configurations and provide basic data visualization and querying.
    """
    def __init__(self, config=None):
        # Optional config dictionary
        self.config = config if config else {}
        self.data = None

    # ----- Basic column visualization -----
    def plot_histogram(self, column):
        """Plot histogram for a numeric column."""
        if self.data is not None and column in self.data.columns:
            plt.figure(figsize=(8, 5))
            sns.histplot(self.data[column], kde=True)
            plt.title(f'Histogram of {column}')
            plt.show()
        else:
            print(f"Column '{column}' not found or no data loaded.")

    def plot_line(self, x_column, y_column):
        """Plot line graph for numeric data."""
        if self.data is not None and x_column in self.data.columns and y_column in self.data.columns:
            plt.figure(figsize=(8, 5))
            plt.plot(self.data[x_column], self.data[y_column], marker='o')
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f'Line plot: {y_column} vs {x_column}')
            plt.show()
        else:
            print("Columns not found or no data loaded.")

    # ----- Simple query -----
    def query_simple(self, column, value):
        """Return rows where column equals value (simple condition)."""
        if self.data is not None and column in self.data.columns:
            result = self.data[self.data[column] == value]
            return result
        else:
            print("Column not found or no data loaded.")
            return pd.DataFrame()


# ===== Child Class =====
class CSVDataProcessor(DataVisualizer):
    """
    Child class to read CSV, store dataframe, use configuration, and provide advanced visualization.
    """
    def __init__(self, csv_file, config=None):
        super().__init__(config)
        self.csv_file = csv_file
        self.read_data()

    def read_data(self):
        """Read CSV into dataframe."""
        try:
            self.data = pd.read_csv(self.csv_file)
            print(f"Data loaded successfully. Shape: {self.data.shape}")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = None

    # ----- Advanced Visualizations -----
    def plot_violin(self, column):
        if self.data is not None and column in self.data.columns:
            plt.figure(figsize=(8, 5))
            sns.violinplot(y=self.data[column])
            plt.title(f'Violin plot of {column}')
            plt.show()
        else:
            print(f"Column '{column}' not found or no data loaded.")

    def plot_box(self, column):
        if self.data is not None and column in self.data.columns:
            plt.figure(figsize=(8, 5))
            sns.boxplot(y=self.data[column])
            plt.title(f'Boxplot of {column}')
            plt.show()
        else:
            print(f"Column '{column}' not found or no data loaded.")

    def plot_scatter(self, x_column, y_column):
        if self.data is not None and x_column in self.data.columns and y_column in self.data.columns:
            plt.figure(figsize=(8, 5))
            sns.scatterplot(x=self.data[x_column], y=self.data[y_column])
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f'Scatter plot: {y_column} vs {x_column}')
            plt.show()
        else:
            print("Columns not found or no data loaded.")

    # ----- Boolean indexing query -----
    def query_boolean(self, conditions: dict):
        """
        Query multiple conditions.
        conditions: dict -> {column_name: value or list of values}
        """
        if self.data is None:
            print("No data loaded.")
            return pd.DataFrame()

        df = self.data
        for col, val in conditions.items():
            if col in df.columns:
                if isinstance(val, list):
                    df = df[df[col].isin(val)]
                else:
                    df = df[df[col] == val]
            else:
                print(f"Column '{col}' not found, skipping.")
        return df
