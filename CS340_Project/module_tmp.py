import os
import numpy as np
import pandas as pd

# Global immutable constant (tuple)
DEFAULT_SHAPE = (3, 4)

# Global mutable container
GLOBAL_LOG = []


def make_numpy_dataframe(rows, cols, start=0):
    """Create a NumPy m x n array and write it into a DataFrame."""
    arr = np.arange(start, start + rows * cols).reshape(rows, cols)
    df = pd.DataFrame(arr, columns=[f"c{i}" for i in range(cols)])
    return df


def export_dataframe_pickle(df, path):
    """Export a DataFrame to a pickle file with basic error handling."""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        df.to_pickle(path)
        return True
    except Exception as exc:
        GLOBAL_LOG.append(f"Pickle export failed: {exc}")
        return False


def safe_eval(expression, **kwargs):
    """Evaluate a simple expression using restricted globals."""
    try:
        return eval(expression, {"__builtins__": {}}, kwargs)
    except Exception as exc:
        GLOBAL_LOG.append(f"Eval failed: {exc}")
        return None


def apply_transformations(values, *funcs):
    """Apply a sequence of callables to a list of values."""
    result = list(values)
    for func in funcs:
        result = [func(v) for v in result]
    return result


def summarize_with_kwargs(df, **kwargs):
    """Demonstrate **kwargs usage with DataFrame.describe."""
    return df.describe(**kwargs)


def make_counter():
    """Create a counter function using a nonlocal variable."""
    count = 0

    def inc():
        nonlocal count
        count += 1
        return count

    return inc


class TempCache:
    """Simple cache class with private-like variable."""

    def __init__(self):
        self._cache = {}

    def set(self, key, value):
        self._cache[key] = value

    def get(self, key, default=None):
        return self._cache.get(key, default)
