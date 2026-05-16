import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BusinessLens AI", layout="wide")

st.title("📊 BusinessLens AI")
st.subheader("AI-Powered Business Analyst Assistant")

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file, encoding="latin1")

    # Success message
    st.success("CSV uploaded successfully!")

    # Dataset preview
    st.write("## Dataset Preview")
    st.dataframe(df.head())

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    # Missing values
    st.write("## Missing Values")

    missing_values = df.isnull().sum()

    st.dataframe(
        missing_values.reset_index().rename(
            columns={
                "index": "Column",
                0: "Missing Values"
            }
        )
    )

    # Statistics
    st.write("## Basic Statistics")
    st.dataframe(df.describe())

    # Column types
    st.write("## Column Types")

    numeric_columns = df.select_dtypes(include=["number"]).columns
    categorical_columns = df.select_dtypes(exclude=["number"]).columns

    col3, col4 = st.columns(2)

    with col3:
        st.write("### Numeric Columns")
        st.write(list(numeric_columns))

    with col4:
        st.write("### Categorical Columns")
        st.write(list(categorical_columns))

    # =========================
    # VISUAL ANALYTICS
    # =========================

    st.write("## Visual Analytics")

    # Sales Histogram
    if "SALES" in df.columns:

        st.write("### Sales Distribution")

        fig_sales = px.histogram(
            df,
            x="SALES",
            nbins=30,
            title="Distribution of Sales"
        )

        st.plotly_chart(
            fig_sales,
            use_container_width=True
        )

    # Top Countries by Sales
    if "COUNTRY" in df.columns and "SALES" in df.columns:

        st.write("### Top Countries by Sales")

        country_sales = (
            df.groupby("COUNTRY")["SALES"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig_country = px.bar(
            country_sales,
            x="COUNTRY",
            y="SALES",
            title="Top 10 Countries by Total Sales"
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )

    # Product Line Pie Chart
    if "PRODUCTLINE" in df.columns and "SALES" in df.columns:

        st.write("### Sales by Product Line")

        product_sales = (
            df.groupby("PRODUCTLINE")["SALES"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig_product = px.pie(
            product_sales,
            names="PRODUCTLINE",
            values="SALES",
            title="Sales Share by Product Line"
        )

        st.plotly_chart(
            fig_product,
            use_container_width=True
        )

    # Correlation matrix
    st.write("## Correlation Matrix")

    if len(numeric_columns) > 1:

        correlation_matrix = df[numeric_columns].corr()

        st.dataframe(correlation_matrix)

    else:
        st.warning(
            "Not enough numeric columns for correlation analysis."
        )

else:
    st.info("Please upload a CSV file to start analysis.")
