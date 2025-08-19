import streamlit as st
import pandas as pd
from UAM import modeling

def show():
    st.title("Modeling Module")

    st.write("Upload your dataset (CSV format) for modeling:")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Data preview:")
            st.dataframe(df.head())

            target_col = st.text_input("Enter the target column name (optional):")

            if st.button("Run Modeling"):
                with st.spinner("Running modeling..."):
                    modeling.run_modeling(df, provided_target=target_col if target_col else None)
                st.success("Modeling completed. Check the reports directory for results.")
        except Exception as e:
            st.error(f"Error loading or processing file: {e}")
