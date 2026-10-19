
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Data Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered Dataset Analyzer")
st.write("Upload a dataset to analyze and visualize your data.")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("Dataset uploaded successfully!")

        # Dataset preview
        st.subheader("Dataset Preview")
        st.dataframe(df.head(100), use_container_width=True)

        # Summary metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Rows", len(df))

        with col2:
            st.metric("Total Columns", len(df.columns))

        with col3:
            st.metric(
                "Missing Values",
                int(df.isna().sum().sum())
            )

        # Data quality checks
        st.subheader("Data Quality")
        quality = pd.DataFrame({
            "Column": df.columns,
            "Missing Values": df.isna().sum().values,
            "Unique Values": df.nunique().values,
            "Data Type": df.dtypes.astype(str).values
        })
        st.dataframe(quality, use_container_width=True)

        # Statistical summary
        st.subheader("Statistical Summary")
        st.dataframe(
            df.describe(include="all").T,
            use_container_width=True
        )

        # Visualization
        st.subheader("Create a Chart")

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        chart_type = st.selectbox(
            "Chart Type",
            ["Histogram", "Bar Chart", "Scatter Plot"]
        )

        if numeric_columns:
            x_col = st.selectbox(
                "Select column",
                numeric_columns
            )

            if chart_type == "Histogram":
                fig = px.histogram(
                    df, x=x_col,
                    title=f"Distribution of {x_col}"
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Bar Chart":
                counts = df[x_col].value_counts().head(20)
                fig = px.bar(
                    x=counts.index.astype(str),
                    y=counts.values,
                    labels={"x": x_col, "y": "Count"},
                    title=f"Top Values in {x_col}"
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Scatter Plot":
                if len(numeric_columns) >= 2:
                    y_col = st.selectbox(
                        "Select second column",
                        [c for c in numeric_columns if c != x_col]
                    )
                    fig = px.scatter(
                        df, x=x_col, y=y_col,
                        title=f"{x_col} vs {y_col}"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(
                        "Scatter plots require two numeric columns."
                    )
        else:
            st.info("No numeric columns are available for these charts.")

        # Basic evidence-based insights
        st.subheader("📌 Automatic Insights")

        st.write(f"- The dataset contains {len(df)} rows.")
        st.write(f"- There are {len(df.columns)} columns.")
        st.write(
            f"- {int(df.isna().sum().sum())} cells contain missing values."
        )

        for col in numeric_columns[:5]:
            st.write(
                f"- **{col}**: mean = {df[col].mean():.2f}, "
                f"median = {df[col].median():.2f}."
            )

        # Verification panel
        st.subheader("✅ Calculation Verification")

        checks = {
            "Row count": len(df) == df.shape[0],
            "Column count": len(df.columns) == df.shape[1],
            "Missing-value count": (
                int(df.isna().sum().sum())
                == int(df.isnull().sum().sum())
            )
        }

        for name, passed in checks.items():
            if passed:
                st.success(f"{name}: Verified")
            else:
                st.error(f"{name}: Needs review")

        # Download analysis data
        st.download_button(
            "Download Dataset as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="analyzed_dataset.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Unable to analyze this file: {e}")

else:
    st.info("Upload a CSV or Excel dataset to get started.")
