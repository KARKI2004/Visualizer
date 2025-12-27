#Version: v0.1
#Date Last Updated: 12-04-2025

'''
Version: <v0.1>
Description:
< handles CSV data reading, processing, and visualizations>
Authors:
<Samiksha Gnawali, Suyog Karki>
Date Created : <11/08/2025>
'''

#%% IMPORTS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os



class DataVisualizer:
    """
    Parent class to store configurations and provide basic data visualization and querying.
    """
    def __init__(self, config=None):

        self.config = config if config else {}
        self.data = None

    def set_data(self, data):
        """Set an in-memory DataFrame for plotting and queries."""
        self.data = data

    def _save_fig(self, fig, save_path):
        if not save_path:
            return
        out_dir = os.path.dirname(save_path) or "."
        os.makedirs(out_dir, exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")

    def plot_histogram(self, column, show=True, save_path=None):
        """Plot histogram for a numeric column."""
        if self.data is not None and column in self.data.columns:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.histplot(self.data[column], kde=True, ax=ax)
            ax.set_title(f'Histogram of {column}')
            self._save_fig(fig, save_path)
            if show:
                plt.show()
            return fig
        else:
            print(f"Column '{column}' not found or no data loaded.")
            return None

    def plot_line(self, x_column, y_column, show=True, save_path=None):
        """Plot line graph for numeric data."""
        if self.data is not None and x_column in self.data.columns and y_column in self.data.columns:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(self.data[x_column], self.data[y_column], marker='o')
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(f'Line plot: {y_column} vs {x_column}')
            self._save_fig(fig, save_path)
            if show:
                plt.show()
            return fig
        else:
            print("Columns not found or no data loaded.")
            return None

    def plot_violin(self, column, show=True, save_path=None):
        if self.data is not None and column in self.data.columns:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.violinplot(y=self.data[column], ax=ax)
            ax.set_title(f'Violin plot of {column}')
            self._save_fig(fig, save_path)
            if show:
                plt.show()
            return fig
        else:
            print(f"Column '{column}' not found or no data loaded.")
            return None

    def plot_box(self, column, show=True, save_path=None):
        if self.data is not None and column in self.data.columns:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(y=self.data[column], ax=ax)
            ax.set_title(f'Boxplot of {column}')
            self._save_fig(fig, save_path)
            if show:
                plt.show()
            return fig
        else:
            print(f"Column '{column}' not found or no data loaded.")
            return None

    def plot_scatter(self, x_column, y_column, show=True, save_path=None):
        if self.data is not None and x_column in self.data.columns and y_column in self.data.columns:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.scatterplot(x=self.data[x_column], y=self.data[y_column], ax=ax)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(f'Scatter plot: {y_column} vs {x_column}')
            self._save_fig(fig, save_path)
            if show:
                plt.show()
            return fig
        else:
            print("Columns not found or no data loaded.")
            return None

    def query_simple(self, column, value):
        """Return rows where column equals value (simple condition)."""
        if self.data is not None and column in self.data.columns:
            result = self.data[self.data[column] == value]
            return result
        else:
            print("Column not found or no data loaded.")
            return pd.DataFrame()


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

    def plot_histogram(self, column, show=True, save_path=None):
        """Override parent method to add basic logging."""
        fig = super().plot_histogram(column, show=show, save_path=save_path)
        if fig is None:
            self.log(f"Histogram failed for column: {column}")
        return fig

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

    def log(self, message):
        """Append messages to a log file in Output folder."""
        os.makedirs("Output", exist_ok=True)
        with open("Output/log.txt", "a") as f:
            f.write(message + "\n")
