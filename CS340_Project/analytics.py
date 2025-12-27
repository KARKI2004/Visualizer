#Version: v0.1
#Date Last Updated: 12-04-2025

'''
Version: <v0.1>
Description:
<Handles computation, probability, and vector analysis using pickle data>
Authors:
<Samiksha Gnawali, Suyog Karki>
Date Created : <11/30/2025>
'''

#%% IMPORTS
import pandas as pd
import numpy as np
import pickle
import math
import os
from itertools import permutations, combinations
from config import CONFIG


# PARENT CLASS: VectorAnalyzer
class VectorAnalyzer:
    """Parent class to handle pickle reading, basic vector operations, and export."""

    def __init__(self, pickle_file=None, data=None):
        self.pickle_file = pickle_file
        self.data = data

    def set_data(self, data):
        """Set an in-memory DataFrame for analysis."""
        self.data = data

    def read_pickle(self):
        """Read pickle file into a DataFrame."""
        if not self.pickle_file:
            print("No pickle file provided.")
            return
        try:
            with open(self.pickle_file, "rb") as f:
                self.data = pickle.load(f)
            print(f"Pickle loaded successfully. Shape: {self.data.shape}")
        except Exception as e:
            print(f"Error loading pickle: {e}")
            self.data = None

    def show_summary(self, export=True):
        """Show and export summary statistics."""
        if isinstance(self.data, pd.DataFrame):
            print("\n=== Summary Statistics ===")
            print(self.data.describe())
            if export:
                os.makedirs("Output", exist_ok=True)
                self.data.describe().to_csv("Output/pickle_summary.csv", index=False)
                print("Summary exported to Output/pickle_summary.csv")
        else:
            print("No valid DataFrame loaded.")

    def vector_operations(self, a, b, export=True):
        """Compute basic vector operations and export results."""
        a, b = np.array(a), np.array(b)
        dot = np.dot(a, b)
        mag_a, mag_b = np.linalg.norm(a), np.linalg.norm(b)

        if mag_a == 0 or mag_b == 0:
            angle = None
            orthogonal = "Undefined"
            unit_a = None
            unit_b = None
            proj_a_on_b = None
        else:
            cos_theta = dot / (mag_a * mag_b)
            cos_theta = max(min(cos_theta, 1.0), -1.0)
            angle = math.degrees(math.acos(cos_theta))
            orthogonal = "Yes" if abs(dot) < 1e-6 else "No"
            unit_a = a / mag_a
            unit_b = b / mag_b
            proj_a_on_b = (dot / mag_b**2) * b

        angle_display = f"{angle:.2f} deg" if angle is not None else "Undefined"

        print("\n=== Vector Operations ===")
        print(f"Vector A: {a}")
        print(f"Vector B: {b}")
        print(f"Dot Product: {dot}")
        print(f"Angle: {angle_display}")
        print(f"Orthogonal? {orthogonal}")
        print(f"Unit Vector A: {unit_a}")
        print(f"Unit Vector B: {unit_b}")
        print(f"Projection of A on B: {proj_a_on_b}")

        results = pd.DataFrame({
            "Operation": [
                "Dot Product", "Angle (deg)", "Orthogonal",
                "Unit Vector A", "Unit Vector B", "Projection (A on B)"
            ],
            "Result": [
                dot,
                angle,
                orthogonal,
                unit_a.tolist() if unit_a is not None else None,
                unit_b.tolist() if unit_b is not None else None,
                proj_a_on_b.tolist() if proj_a_on_b is not None else None
            ]
        })

        if export:
            os.makedirs("Output", exist_ok=True)
            results.to_csv("Output/vector_results.csv", index=False)
            print("Vector results exported to Output/vector_results.csv")
        return results


# CHILD CLASS: ProbabilityAnalyzer
class ProbabilityAnalyzer(VectorAnalyzer):
    """Child class extending VectorAnalyzer with probability and categorical analysis."""

    def show_summary(self, export=True):
        """Override parent summary to keep interface consistent for children."""
        return super().show_summary(export=export)

    def _validate_columns(self, *cols):
        if self.data is None:
            print("No data loaded.")
            return False
        missing = [c for c in cols if c not in self.data.columns]
        if missing:
            print(f"Columns not found: {missing}")
            return False
        return True

    def joint_counts(self, col1, col2, export=True):
        if self._validate_columns(col1, col2):
            joint = pd.crosstab(self.data[col1], self.data[col2])
            print("\n=== Joint Counts ===")
            print(joint)
            if export:
                os.makedirs("Output", exist_ok=True)
                joint.to_csv("Output/joint_counts.csv")
                print("Joint counts exported.")
            return joint
        return None

    def joint_probability(self, col1, col2, export=True):
        if self._validate_columns(col1, col2):
            joint = pd.crosstab(self.data[col1], self.data[col2]) / len(self.data)
            print("\n=== Joint Probability Table ===")
            print(joint)
            if export:
                os.makedirs("Output", exist_ok=True)
                joint.to_csv("Output/joint_probability.csv")
                print("Joint probabilities exported.")
            return joint
        return None

    def conditional_probability(self, col1, col2, export=True):
        if self._validate_columns(col1, col2):
            cond = pd.crosstab(self.data[col1], self.data[col2], normalize='columns')
            print("\n=== Conditional Probability Table ===")
            print(cond)
            if export:
                os.makedirs("Output", exist_ok=True)
                cond.to_csv("Output/conditional_probability.csv")
                print("Conditional probabilities exported.")
            return cond
        return None

    def categorical_analysis(self, col, export=True):
        if self.data is None:
            print("No data loaded.")
            return None
        if col not in self.data.columns:
            print(f"Column '{col}' not found.")
            return None
        vals = self.data[col].dropna().unique()
        perms = list(permutations(vals, 2))[:5]
        combs = list(combinations(vals, 2))[:5]

        print(f"\nUnique values in {col}: {vals}")
        print(f"2-permutations (first 5): {perms}")
        print(f"2-combinations (first 5): {combs}")
        if export:
            os.makedirs("Output", exist_ok=True)
            with open("Output/categorical_analysis.txt", "w") as f:
                f.write(f"Unique values in {col}: {vals}\n")
                f.write(f"2-permutations: {perms}\n")
                f.write(f"2-combinations: {combs}\n")
            print("Categorical analysis exported.")

        return {
            "unique_values": vals,
            "permutations_2": perms,
            "combinations_2": combs
        }
