import os
import sys
import pickle
import pandas as pd
import streamlit as st

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(ROOT_DIR, "CS340_Project")
sys.path.append(PROJECT_DIR)

from data_handler import DataVisualizer
from analytics import ProbabilityAnalyzer


def load_data(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith(".pkl") or name.endswith(".pickle"):
        return pickle.load(uploaded_file)
    return None


def safe_name(name):
    return "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in name)


st.set_page_config(page_title="Dataset Analysis", layout="wide")
st.title("Dataset Analysis Tool")
st.write("Upload a CSV or pickle file and select columns for analysis and visualization.")

uploaded = st.file_uploader("Upload CSV or pickle", type=["csv", "pkl", "pickle"])

if not uploaded:
    st.info("Upload a CSV or pickle file to begin.")
    st.stop()

data = load_data(uploaded)
if data is None:
    st.error("Unsupported file type.")
    st.stop()
if not isinstance(data, pd.DataFrame):
    st.error("Uploaded pickle does not contain a pandas DataFrame.")
    st.stop()

df = data

st.success(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
st.dataframe(df.head(20))

numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = [c for c in df.columns if c not in numeric_cols]
all_cols = df.columns.tolist()

output_dir = os.path.join(ROOT_DIR, "Output")
save_outputs = st.sidebar.checkbox("Save outputs to Output/", value=True)

viz = DataVisualizer()
viz.set_data(df)
analyzer = ProbabilityAnalyzer(data=df)

st.header("Summary")
summary_df = df.describe()
st.dataframe(summary_df)

st.header("Plots")
if not numeric_cols:
    st.warning("No numeric columns found for plots.")
else:
    show_hist = st.checkbox("Show histogram")
    if show_hist:
        hist_col = st.selectbox("Histogram column", numeric_cols, key="hist_col")
        save_path = None
        if save_outputs:
            save_path = os.path.join(output_dir, f"histogram_{safe_name(hist_col)}.png")
        fig = viz.plot_histogram(hist_col, show=False, save_path=save_path)
        if fig:
            st.pyplot(fig)

    show_line = st.checkbox("Show line plot")
    if show_line:
        x_col = st.selectbox("Line X column", numeric_cols, key="line_x")
        y_col = st.selectbox("Line Y column", numeric_cols, key="line_y")
        save_path = None
        if save_outputs:
            save_path = os.path.join(output_dir, f"line_{safe_name(x_col)}_{safe_name(y_col)}.png")
        fig = viz.plot_line(x_col, y_col, show=False, save_path=save_path)
        if fig:
            st.pyplot(fig)

    show_violin = st.checkbox("Show violin plot")
    if show_violin:
        violin_col = st.selectbox("Violin column", numeric_cols, key="violin_col")
        save_path = None
        if save_outputs:
            save_path = os.path.join(output_dir, f"violin_{safe_name(violin_col)}.png")
        fig = viz.plot_violin(violin_col, show=False, save_path=save_path)
        if fig:
            st.pyplot(fig)

    show_box = st.checkbox("Show box plot")
    if show_box:
        box_col = st.selectbox("Box column", numeric_cols, key="box_col")
        save_path = None
        if save_outputs:
            save_path = os.path.join(output_dir, f"box_{safe_name(box_col)}.png")
        fig = viz.plot_box(box_col, show=False, save_path=save_path)
        if fig:
            st.pyplot(fig)

    show_scatter = st.checkbox("Show scatter plot")
    if show_scatter:
        scatter_x = st.selectbox("Scatter X column", numeric_cols, key="scatter_x")
        scatter_y = st.selectbox("Scatter Y column", numeric_cols, key="scatter_y")
        save_path = None
        if save_outputs:
            save_path = os.path.join(output_dir, f"scatter_{safe_name(scatter_x)}_{safe_name(scatter_y)}.png")
        fig = viz.plot_scatter(scatter_x, scatter_y, show=False, save_path=save_path)
        if fig:
            st.pyplot(fig)

st.header("Probability Tables")
if len(all_cols) < 2:
    st.warning("Need at least two columns for probability tables.")
else:
    col1 = st.selectbox("Column 1", all_cols, key="prob_col1")
    col2 = st.selectbox("Column 2", all_cols, key="prob_col2")

    show_joint = st.checkbox("Show joint counts")
    if show_joint:
        joint = analyzer.joint_counts(col1, col2, export=save_outputs)
        if joint is not None:
            st.dataframe(joint)

    show_joint_prob = st.checkbox("Show joint probability")
    if show_joint_prob:
        joint_prob = analyzer.joint_probability(col1, col2, export=save_outputs)
        if joint_prob is not None:
            st.dataframe(joint_prob)

    show_cond = st.checkbox("Show conditional probability")
    if show_cond:
        cond = analyzer.conditional_probability(col1, col2, export=save_outputs)
        if cond is not None:
            st.dataframe(cond)

st.header("Vector Operations")
if len(numeric_cols) < 2:
    st.warning("Need at least two numeric columns for vector operations.")
else:
    vec_col_a = st.selectbox("Vector A column", numeric_cols, key="vec_a")
    vec_col_b = st.selectbox("Vector B column", numeric_cols, key="vec_b")
    max_len = min(100, len(df))
    vec_len = st.slider("Number of rows", min_value=2, max_value=max_len, value=min(5, max_len))
    show_vec = st.checkbox("Run vector operations")
    if show_vec:
        vec_a = df[vec_col_a].values[:vec_len]
        vec_b = df[vec_col_b].values[:vec_len]
        vec_results = analyzer.vector_operations(vec_a, vec_b, export=save_outputs)
        st.dataframe(vec_results)

st.header("Categorical Analysis")
if not all_cols:
    st.warning("No columns available for categorical analysis.")
else:
    cat_col = st.selectbox("Column", all_cols, key="cat_col")
    show_cat = st.checkbox("Run categorical analysis")
    if show_cat:
        cat_results = analyzer.categorical_analysis(cat_col, export=save_outputs)
        if cat_results:
            st.write("Unique values:", cat_results["unique_values"])
            st.write("2-permutations (first 5):", cat_results["permutations_2"])
            st.write("2-combinations (first 5):", cat_results["combinations_2"])
