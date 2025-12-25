import os
import sys
import pickle
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

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

def df_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")

def fig_to_png_bytes(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf


st.set_page_config(page_title="Dataset Analysis", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stFileUploader"] {
        background: #f8d7da;
        border: 1px dashed #c94f5e;
        border-radius: 10px;
        padding: 18px 16px;
    }
    [data-testid="stFileUploader"] section {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    [data-testid="stFileUploader"] button {
        background: transparent;
        border: none;
        color: #6b1b1b;
        font-weight: 700;
        font-size: 18px;
        padding: 0;
        flex: 1;
        text-align: center;
    }
    [data-testid="stFileUploader"] small {
        color: #6b1b1b;
    }
    [data-testid="stSidebar"] .stVerticalBlock {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .sidebar-spacer {
        flex: 1 1 auto;
    }
    .section-box {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 18px;
        background: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Visualizer")
st.write("Upload a CSV or pickle file and select columns for analysis and visualization.")

uploaded = st.file_uploader(
    "Upload file",
    type=["csv", "pkl", "pickle"],
    help="Drag and drop here",
)

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

st.sidebar.header("Missing Value Handling")
missing_option = st.sidebar.selectbox(
    "Choose a missing value strategy",
    [
        "None",
        "Drop rows with missing values",
        "Fill numeric NaNs with mean",
        "Fill numeric NaNs with median",
        "Fill categorical NaNs with 'Unknown'",
        "Custom fill value (single column)",
    ],
)
custom_value = None
custom_column = None
if missing_option == "Custom fill value (single column)":
    custom_value = st.sidebar.text_input("Custom fill value (applies to NaNs only)", value="")
    custom_column = st.sidebar.selectbox(
        "Apply to column",
        df.columns.tolist(),
    )

df_clean = df.copy()
if missing_option == "Drop rows with missing values":
    df_clean = df_clean.dropna()
elif missing_option == "Fill numeric NaNs with mean":
    num_cols = df_clean.select_dtypes(include="number").columns
    df_clean[num_cols] = df_clean[num_cols].fillna(df_clean[num_cols].mean())
elif missing_option == "Fill numeric NaNs with median":
    num_cols = df_clean.select_dtypes(include="number").columns
    df_clean[num_cols] = df_clean[num_cols].fillna(df_clean[num_cols].median())
elif missing_option == "Fill categorical NaNs with 'Unknown'":
    cat_cols = df_clean.select_dtypes(exclude="number").columns
    df_clean[cat_cols] = df_clean[cat_cols].fillna("Unknown")
elif missing_option == "Custom fill value (single column)":
    if custom_value is not None and custom_column:
        col = custom_column
        if pd.api.types.is_numeric_dtype(df_clean[col]):
            try:
                df_clean[col] = df_clean[col].fillna(float(custom_value))
            except ValueError:
                df_clean[col] = df_clean[col].fillna(custom_value)
        else:
            df_clean[col] = df_clean[col].fillna(custom_value)

st.success(f"Loaded {df_clean.shape[0]} rows and {df_clean.shape[1]} columns.")
st.dataframe(df_clean.head(20))

numeric_cols = df_clean.select_dtypes(include="number").columns.tolist()
categorical_cols = [c for c in df_clean.columns if c not in numeric_cols]
all_cols = df_clean.columns.tolist()

output_dir = os.path.join(ROOT_DIR, "Output")
save_outputs = st.sidebar.checkbox("Save outputs to Output/", value=True)

viz = DataVisualizer()
viz.set_data(df_clean)
analyzer = ProbabilityAnalyzer(data=df_clean)

st.markdown('<a id="summary"></a>', unsafe_allow_html=True)
st.header("Summary")
st.markdown('<div class="section-box">', unsafe_allow_html=True)
summary_df = df_clean.describe()
st.dataframe(summary_df)
st.download_button(
    label="Download summary CSV",
    data=df_to_csv_bytes(summary_df),
    file_name="summary.csv",
    mime="text/csv",
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<a id="missing-values"></a>', unsafe_allow_html=True)
st.header("Missing Values")
st.markdown('<div class="section-box">', unsafe_allow_html=True)
missing_before = df.isna().sum().to_frame("missing_count")
missing_after = df_clean.isna().sum().to_frame("missing_count")
st.write("Before handling")
st.dataframe(missing_before[missing_before["missing_count"] > 0])
st.write("After handling")
st.dataframe(missing_after[missing_after["missing_count"] > 0])
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<a id="plots"></a>', unsafe_allow_html=True)
st.header("Plots")
st.markdown('<div class="section-box">', unsafe_allow_html=True)
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
            st.download_button(
                label="Download histogram PNG",
                data=fig_to_png_bytes(fig),
                file_name=f"histogram_{safe_name(hist_col)}.png",
                mime="image/png",
            )

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
            st.download_button(
                label="Download line plot PNG",
                data=fig_to_png_bytes(fig),
                file_name=f"line_{safe_name(x_col)}_{safe_name(y_col)}.png",
                mime="image/png",
            )

    show_violin = st.checkbox("Show violin plot")
    if show_violin:
        violin_col = st.selectbox("Violin column", numeric_cols, key="violin_col")
        save_path = None
        if save_outputs:
            save_path = os.path.join(output_dir, f"violin_{safe_name(violin_col)}.png")
        fig = viz.plot_violin(violin_col, show=False, save_path=save_path)
        if fig:
            st.pyplot(fig)
            st.download_button(
                label="Download violin plot PNG",
                data=fig_to_png_bytes(fig),
                file_name=f"violin_{safe_name(violin_col)}.png",
                mime="image/png",
            )

    show_box = st.checkbox("Show box plot")
    if show_box:
        box_col = st.selectbox("Box column", numeric_cols, key="box_col")
        save_path = None
        if save_outputs:
            save_path = os.path.join(output_dir, f"box_{safe_name(box_col)}.png")
        fig = viz.plot_box(box_col, show=False, save_path=save_path)
        if fig:
            st.pyplot(fig)
            st.download_button(
                label="Download box plot PNG",
                data=fig_to_png_bytes(fig),
                file_name=f"box_{safe_name(box_col)}.png",
                mime="image/png",
            )

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
            st.download_button(
                label="Download scatter plot PNG",
                data=fig_to_png_bytes(fig),
                file_name=f"scatter_{safe_name(scatter_x)}_{safe_name(scatter_y)}.png",
                mime="image/png",
            )
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<a id="probability-tables"></a>', unsafe_allow_html=True)
st.header("Probability Tables")
st.markdown('<div class="section-box">', unsafe_allow_html=True)
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
            st.download_button(
                label="Download joint counts CSV",
                data=joint.to_csv().encode("utf-8"),
                file_name="joint_counts.csv",
                mime="text/csv",
            )

    show_joint_prob = st.checkbox("Show joint probability")
    if show_joint_prob:
        joint_prob = analyzer.joint_probability(col1, col2, export=save_outputs)
        if joint_prob is not None:
            st.dataframe(joint_prob)
            st.download_button(
                label="Download joint probability CSV",
                data=joint_prob.to_csv().encode("utf-8"),
                file_name="joint_probability.csv",
                mime="text/csv",
            )

    show_cond = st.checkbox("Show conditional probability")
    if show_cond:
        cond = analyzer.conditional_probability(col1, col2, export=save_outputs)
        if cond is not None:
            st.dataframe(cond)
            st.download_button(
                label="Download conditional probability CSV",
                data=cond.to_csv().encode("utf-8"),
                file_name="conditional_probability.csv",
                mime="text/csv",
            )
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<a id="vector-operations"></a>', unsafe_allow_html=True)
st.header("Vector Operations")
st.markdown('<div class="section-box">', unsafe_allow_html=True)
if len(numeric_cols) < 2:
    st.warning("Need at least two numeric columns for vector operations.")
else:
    vec_col_a = st.selectbox("Vector A column", numeric_cols, key="vec_a")
    vec_col_b = st.selectbox("Vector B column", numeric_cols, key="vec_b")
    max_len = min(100, len(df))
    vec_len = st.slider("Number of rows", min_value=2, max_value=max_len, value=min(5, max_len))
    show_vec = st.checkbox("Run vector operations")
    if show_vec:
        vec_a = df_clean[vec_col_a].values[:vec_len]
        vec_b = df_clean[vec_col_b].values[:vec_len]
        vec_results = analyzer.vector_operations(vec_a, vec_b, export=save_outputs)
        st.dataframe(vec_results)
        st.download_button(
            label="Download vector results CSV",
            data=df_to_csv_bytes(vec_results),
            file_name="vector_results.csv",
            mime="text/csv",
        )
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<a id="categorical-analysis"></a>', unsafe_allow_html=True)
st.header("Categorical Analysis")
st.markdown('<div class="section-box">', unsafe_allow_html=True)
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
            cat_text = (
                f"Unique values: {cat_results['unique_values']}\n"
                f"2-permutations (first 5): {cat_results['permutations_2']}\n"
                f"2-combinations (first 5): {cat_results['combinations_2']}\n"
            )
            st.download_button(
                label="Download categorical analysis TXT",
                data=cat_text.encode("utf-8"),
                file_name="categorical_analysis.txt",
                mime="text/plain",
            )
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<a id="correlation-analysis"></a>', unsafe_allow_html=True)
st.header("Correlation Analysis")
st.markdown('<div class="section-box">', unsafe_allow_html=True)
if len(numeric_cols) < 2:
    st.warning("Need at least two numeric columns for correlation analysis.")
else:
    corr = df_clean[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha="right")
    ax.set_yticklabels(numeric_cols)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

    corr_pairs = corr.where(~np.eye(len(corr), dtype=bool)).stack()
    top_corr = corr_pairs.reindex(
        corr_pairs.abs().sort_values(ascending=False).index
    ).head(10)
    top_corr_df = top_corr.reset_index()
    top_corr_df.columns = ["column_1", "column_2", "corr"]
    top_corr_df["abs_corr"] = top_corr_df["corr"].abs()
    st.dataframe(top_corr_df)
st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)
st.sidebar.subheader("Navigate")
st.sidebar.markdown(
    """
    - [Summary](#summary)
    - [Missing Values](#missing-values)
    - [Plots](#plots)
    - [Probability Tables](#probability-tables)
    - [Vector Operations](#vector-operations)
    - [Categorical Analysis](#categorical-analysis)
    - [Correlation Analysis](#correlation-analysis)
    """
)
