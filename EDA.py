import streamlit as st
import pandas as pd
import numpy as np
import io
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Exploratory Data Analysis",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Analyze Your Data")
st.write("Upload a CSV or Excel file to explore your dataset")

# --------------------------------------------------
# FILE UPLOADER
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "📁 Upload Your CSV / Excel File",
    type=["csv", "txt", "xlsx", "xls", "xlsm", "xlsb"]
)

# --------------------------------------------------
# MAIN FILE HANDLING LOGIC
# --------------------------------------------------
if uploaded_file is not None:
    try:
        file_name = uploaded_file.name.lower()

        # =========================
        # EXCEL FILE HANDLING
        # =========================
        if file_name.endswith((".xlsx", ".xls", ".xlsm", ".xlsb")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            st.success("✅ Excel file loaded successfully")

        # =========================
        # CSV / TXT HANDLING
        # =========================
        else:
            raw_text = uploaded_file.read().decode("utf-8", errors="ignore")
            lines = raw_text.splitlines()

            if len(lines) < 2:
                st.error("❌ File does not contain tabular data")
                st.stop()

            header = lines[0]
            possible_seps = [",", ";", "\t", "|"]
            sep = None

            for s in possible_seps:
                if header.count(s) > 1:
                    sep = s
                    break

            if sep is None:
                st.error("❌ File is not delimiter-based text")
                st.stop()

            columns = [c.strip().replace('"', '') for c in header.split(sep)]
            data = []

            for row in lines[1:]:
                values = [v.strip().replace('"', '') for v in row.split(sep)]
                if len(values) == len(columns):
                    data.append(values)

            df = pd.DataFrame(data, columns=columns)
            st.success(f"✅ File reconstructed using separator '{sep}'")

        # Attempt numeric conversion
        df = df.apply(pd.to_numeric, errors="ignore")

    except Exception as e:
        st.error("❌ Unable to parse file structure")
        st.exception(e)
        st.stop()

    # --------------------------------------------------
    # DATA PREVIEW
    # --------------------------------------------------
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # --------------------------------------------------
    # DATA OVERVIEW
    # --------------------------------------------------
    st.subheader("📌 Data Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Duplicate Rows", df.duplicated().sum())

    # --------------------------------------------------
    # DATASET INFO
    # --------------------------------------------------
    st.subheader("ℹ️ Dataset Info")
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    # --------------------------------------------------
    # STATISTICAL SUMMARY
    # --------------------------------------------------
    st.subheader("📊 Statistical Summary")
    st.dataframe(df.describe(include="all"))

    # --------------------------------------------------
    # ENHANCED DATA VISUALIZATION (Dashboard Style)
    # --------------------------------------------------

    st.subheader("📊 Interactive Data Visualization")

    cols = df.columns.tolist()
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    col1, col2, col3 = st.columns(3)

    with col1:
        x_col = st.selectbox("Select X Axis", cols)

    with col2:
        y_col = st.selectbox("Select Y Axis (Numeric Recommended)", numeric_cols)

    with col3:
        legend_col = st.selectbox("Select Legend / Color Group (Optional)", ["None"] + cols)

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Pie Chart"]
    )

    aggregation = st.selectbox(
        "Aggregation Method (Optional)",
        ["None", "Sum", "Mean", "Count"]
    )

    plot_df = df.copy()

    # ----------------------------
    # Chart Rendering
    # ----------------------------

    fig = None
    color_arg = None if legend_col == "None" else legend_col

    if chart_type == "Bar Chart":
        fig = px.bar(plot_df, x=x_col, y=y_col, color=color_arg, barmode="group")

    elif chart_type == "Line Chart":
        fig = px.line(plot_df, x=x_col, y=y_col, color=color_arg)

    elif chart_type == "Scatter Plot":
        fig = px.scatter(plot_df, x=x_col, y=y_col, color=color_arg)

    elif chart_type == "Histogram":
        fig = px.histogram(plot_df, x=x_col, color=color_arg)

    elif chart_type == "Box Plot":
        fig = px.box(plot_df, x=x_col, y=y_col, color=color_arg)

    elif chart_type == "Pie Chart":
        fig = px.pie(plot_df, names=x_col, values=y_col if aggregation != "None" else None)

    if fig:
        fig.update_layout(
            template="plotly_white",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("⬆️ Upload a file to begin")