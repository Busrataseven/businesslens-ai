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

    df = pd.read_csv(uploaded_file, encoding="latin1")

    st.success("CSV uploaded successfully!")

    st.write("## Dataset Preview")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

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

    st.write("## Basic Statistics")
    st.dataframe(df.describe())

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

    st.write("## Visual Analytics")

    if "SALES" in df.columns:
        st.write("### Sales Distribution")

        fig_sales = px.histogram(
            df,
            x="SALES",
            nbins=30,
            title="Distribution of Sales"
        )

        st.plotly_chart(fig_sales, use_container_width=True)

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

        st.plotly_chart(fig_country, use_container_width=True)

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

        st.plotly_chart(fig_product, use_container_width=True)

    st.write("## Correlation Matrix")

    if len(numeric_columns) > 1:
        correlation_matrix = df[numeric_columns].corr()
        st.dataframe(correlation_matrix)
    else:
        st.warning("Not enough numeric columns for correlation analysis.")

    st.write("## Business Insights")

    if "COUNTRY" in df.columns and "SALES" in df.columns:
        top_country_row = country_sales.iloc[0]
        top_country = top_country_row["COUNTRY"]
        top_country_sales = top_country_row["SALES"]

        st.success(
            f"🌍 Top performing country is **{top_country}** "
            f"with total sales of **${top_country_sales:,.0f}**."
        )

    if "PRODUCTLINE" in df.columns and "SALES" in df.columns:
        top_product_row = product_sales.iloc[0]
        top_product = top_product_row["PRODUCTLINE"]
        top_product_sales = top_product_row["SALES"]

        st.success(
            f"🏆 Best-selling product line is **{top_product}** "
            f"with total sales of **${top_product_sales:,.0f}**."
        )

    if "SALES" in df.columns:
        average_sales = df["SALES"].mean()
        max_sales = df["SALES"].max()

        st.info(
            f"📊 Average order sales value is **${average_sales:,.0f}**, "
            f"while the highest order sales value is **${max_sales:,.0f}**."
        )

else:
    st.info("Please upload a CSV file to start analysis.")
