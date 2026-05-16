import streamlit as st
import pandas as pd

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

    st.write("## Correlation Matrix")

    if len(numeric_columns) > 1:
        correlation_matrix = df[numeric_columns].corr()
        st.dataframe(correlation_matrix)
    else:
        st.warning("Not enough numeric columns for correlation analysis.")

else:
    st.info("Please upload a CSV file to start analysis.")
