import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        body { background-color: #232323; color: #fafafa; }
        .stApp { background-color: #222; }
        h1, h2, h3, h4, h5, h6 { color: #E0E0E0; }
        .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Exploratory Data Analysis Dashboard")
st.markdown(
    "Upload your CSV or Excel file and instantly explore your data with beautiful, interactive plots powered by Plotly and Altair."
)

# --- SIDEBAR ---
st.sidebar.header("Upload & Settings")
uploaded = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
sample_rows = st.sidebar.slider("Sample rows to show", 5, 50, 10)
theme = st.sidebar.selectbox("Plotly Theme", ["plotly_dark", "plotly", "ggplot2", "seaborn", "viridis"])

if uploaded:
    # --- LOAD DATA ---
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)
    st.success(f"Loaded `{uploaded.name}` ({df.shape[0]} rows, {df.shape[1]} columns)")

    # --- DATA OVERVIEW ---
    st.header("🗂 Data Overview")
    st.write(f"**Rows:** {df.shape[0]} &nbsp; **Columns:** {df.shape[1]}")
    st.dataframe(df.head(sample_rows), use_container_width=True)

    # --- DATA INFO ---
    st.subheader("🔎 Data Info")
    def df_info_as_dataframe(df):
        info = pd.DataFrame({
            "Column": df.columns,
            "Non-Null Count": df.notnull().sum().values,
            "Dtype": df.dtypes.astype(str).values
        })
        return info
    st.dataframe(df_info_as_dataframe(df), use_container_width=True)

    # --- SUMMARY STATS ---
    st.subheader("📈 Summary Statistics")
    st.dataframe(df.describe(include='all').T, use_container_width=True)

    # --- CORRELATION HEATMAP ---
    num_cols = df.select_dtypes(include=np.number).columns
    if len(num_cols) > 1:
        st.subheader("🌈 Correlation Heatmap")
        corr = df[num_cols].corr()
        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu",
            zmin=-1, zmax=1,
            title="Correlation Matrix",
            aspect="auto",
            labels=dict(color="Correlation"),
            width=1100,
            height=900,
        )
        fig.update_layout(
            template=theme,
            xaxis_title="",
            yaxis_title="",
            margin=dict(l=50, r=50, t=50, b=50),
        )
        fig.update_xaxes(side="bottom", tickangle=45, automargin=True)
        fig.update_yaxes(automargin=True)
        st.plotly_chart(fig, use_container_width=True)

    # --- MAIN TABS ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "Distribution", "Time Series", "Scatter", "Column Analyzer"
    ])

    # --- DISTRIBUTION / HISTOGRAM TAB ---
    with tab1:
        st.subheader("Histogram / Distribution")

        # Select numeric column for histogram
        col = st.selectbox("Select numeric column", num_cols, key="hist_col")

        # Number of bins slider
        bins = st.slider("Number of bins", min_value=5, max_value=100, value=30)

        # Categorical columns for color (with ≤ 20 unique values)
        MAX_UNIQUES = 20
        categorical_cols = [
            c for c in df.select_dtypes(include=['object', 'category', 'bool']).columns
            if df[c].nunique(dropna=False) <= MAX_UNIQUES
        ]

        if categorical_cols:
            color_col = st.selectbox("Color bars by (optional)", [None] + categorical_cols, key="hist_color")
        else:
            color_col = None
            st.info(f"No categorical columns with ≤{MAX_UNIQUES} unique values available for coloring.")

        # Plotly histogram
        fig = px.histogram(
            df, 
            x=col,
            nbins=bins,
            color=color_col if color_col else None,
            color_discrete_sequence=px.colors.qualitative.Plotly if color_col else None,
            opacity=0.8,
            title=f"Histogram of {col}" + (f" colored by {color_col}" if color_col else ""),
            template=theme,
            marginal="box",  # Adds a little boxplot on top for extra insight
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- TIME SERIES TAB ---
    with tab2:
        st.subheader("Time Series Plot")
        time_cols = [c for c in df.columns if np.issubdtype(df[c].dtype, np.datetime64)] + \
                    [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()]
        x_col = st.selectbox("Select time/date column", time_cols if time_cols else df.columns, key="ts_x")
        y_col = st.selectbox("Select numeric column", num_cols, key="ts_y")
        fig = px.line(df, x=x_col, y=y_col, template=theme, markers=True)
        st.plotly_chart(fig, use_container_width=True)

    # --- SCATTER TAB ---
    with tab3:
        st.subheader("Scatter Plot (with Color Mapping)")
        x_col = st.selectbox("X-axis", num_cols, key="scatter_x")
        y_col = st.selectbox("Y-axis", num_cols, index=1 if len(num_cols) > 1 else 0, key="scatter_y")
        scatter_cat_cols = [
            None
        ] + list(df.select_dtypes(include=['object', 'category']).columns)
        color_col = st.selectbox("Color by", scatter_cat_cols, key="scatter_color")
        fig = px.scatter(
            df, x=x_col, y=y_col,
            color=color_col if color_col else None,
            color_continuous_scale=theme if color_col is None else None,
            template=theme,
            opacity=0.7,
            marginal_x="histogram", marginal_y="histogram",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- COLUMN ANALYZER TAB ---
    with tab4:
        st.header("🔍 Column Analyzer")
        col_to_analyze = st.selectbox("Select a column to analyze", df.columns, key="analyze_col")
        dtype = df[col_to_analyze].dtype

        if isinstance(dtype, pd.CategoricalDtype) or \
           pd.api.types.is_object_dtype(df[col_to_analyze]) or \
           pd.api.types.is_bool_dtype(df[col_to_analyze]):
            st.markdown("### 🟦 Categorical/Boolean Column")
            unique_count = df[col_to_analyze].nunique(dropna=False)
            st.write(f"**Number of unique values:** `{unique_count}`")
            MAX_TO_SHOW = 100
            value_counts = df[col_to_analyze].value_counts(dropna=False)
            st.write("**Top unique values and their counts:**")
            st.dataframe(value_counts.head(MAX_TO_SHOW))
            if unique_count > MAX_TO_SHOW:
                st.info(f"Column has more than {MAX_TO_SHOW} unique values. Showing only the top {MAX_TO_SHOW}.")
            st.write("**Summary statistics:**")
            st.dataframe(df[[col_to_analyze]].describe(include='all').T)

        elif pd.api.types.is_numeric_dtype(df[col_to_analyze]):
            st.markdown("### 🟩 Numeric Column")
            st.write("**Summary statistics:**")
            st.dataframe(df[[col_to_analyze]].describe().T)
            st.write("**Histogram of values:**")
            st.altair_chart(
                alt.Chart(df).mark_bar(opacity=0.8).encode(
                    x=alt.X(f"{col_to_analyze}:Q", bin=alt.Bin(maxbins=30), title=col_to_analyze),
                    y=alt.Y('count()', title='Frequency'),
                    tooltip=[col_to_analyze, alt.Tooltip('count()', title='Frequency')]
                ).properties(width='container', height=300).interactive(),
                use_container_width=True
            )

        elif pd.api.types.is_datetime64_any_dtype(df[col_to_analyze]):
            st.markdown("### 🟨 Datetime Column")
            st.write(f"**Earliest:** {df[col_to_analyze].min()}")
            st.write(f"**Latest:** {df[col_to_analyze].max()}")
            st.write("**Sample values:**")
            st.dataframe(df[col_to_analyze].drop_duplicates().sort_values().head(10))

        else:
            st.warning("Unsupported column type for this analyzer.")

    # --- DOWNLOAD DATA ---
    st.sidebar.markdown("### Download")
    st.sidebar.download_button("Download processed CSV", df.to_csv(index=False), file_name="processed_data.csv")

else:
    st.info("Upload a dataset to get started! 🎈")
