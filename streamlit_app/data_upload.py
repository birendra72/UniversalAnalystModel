import sys
import os
import pickle
import json
import streamlit as st
import pandas as pd
from streamlit_app.utils.cli_interface import load_data, preprocess_data, run_eda, run_insight_extraction_local, run_modeling, generate_report
from streamlit_app.utils.temp_storage import download_report, download_visualizations

STATE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'streamlit_app', 'state')
os.makedirs(STATE_DIR, exist_ok=True)

DATAFRAME_STATE_FILE = os.path.join(STATE_DIR, 'dataframe.pkl')
PIPELINE_STATUS_FILE = os.path.join(STATE_DIR, 'pipeline_status.json')
FILE_NAME_FILE = os.path.join(STATE_DIR, 'file_name.txt')

def save_state(df, pipeline_status, file_name):
    with open(DATAFRAME_STATE_FILE, 'wb') as f:
        pickle.dump(df, f)
    with open(PIPELINE_STATUS_FILE, 'w') as f:
        json.dump(pipeline_status, f)
    with open(FILE_NAME_FILE, 'w') as f:
        f.write(file_name)

def load_state():
    df = None
    pipeline_status = None
    file_name = None
    try:
        with open(DATAFRAME_STATE_FILE, 'rb') as f:
            df = pickle.load(f)
        with open(PIPELINE_STATUS_FILE, 'r') as f:
            pipeline_status = json.load(f)
        with open(FILE_NAME_FILE, 'r') as f:
            file_name = f.read()
    except Exception:
        pass
    return df, pipeline_status, file_name

def clear_state():
    for file in [DATAFRAME_STATE_FILE, PIPELINE_STATUS_FILE, FILE_NAME_FILE]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

def show():
    st.title("📁 Data Upload")
    st.markdown("Upload your dataset to begin analysis")

    # Load saved state on app start
    if 'df' not in st.session_state or st.session_state.df is None:
        df, pipeline_status, file_name = load_state()
        if df is not None:
            st.session_state.df = df
        if pipeline_status is not None:
            st.session_state.pipeline_status = pipeline_status
        if file_name is not None:
            st.session_state.file_name = file_name

    # Initialize pipeline status if not present
    if 'pipeline_status' not in st.session_state:
        st.session_state.pipeline_status = {
            "Data Loaded": False,
            "Preprocessing": False,
            "EDA": False,
            "Insight Extraction": False,
            "Modeling": False,
            "Report Generation": False
        }

    uploaded_file = st.file_uploader(
        "Upload your dataset (CSV, Excel)", 
        type=["csv", "xlsx", "xls"],
        help="Supported formats: CSV, Excel"
    )

    if st.button("Clear saved state and start fresh"):
        clear_state()
        st.session_state.df = None
        st.session_state.pipeline_status = {
            "Data Loaded": False,
            "Preprocessing": False,
            "EDA": False,
            "Insight Extraction": False,
            "Modeling": False,
            "Report Generation": False
        }
        st.session_state.file_name = None

    if uploaded_file is not None:
        try:
            ext = uploaded_file.name.split('.')[-1].lower()
            if ext == 'csv':
                source_type = 'csv'
            elif ext in ['xlsx', 'xls']:
                source_type = 'xlsx'
            else:
                st.error("Unsupported file format")
                return

            source_config = {'filepath': uploaded_file}
            df = load_data(source_type, source_config)
            st.session_state.df = df
            st.session_state.file_name = uploaded_file.name
            st.session_state.pipeline_status["Data Loaded"] = True
            st.success(f"Successfully loaded {uploaded_file.name} with {df.shape[0]} rows and {df.shape[1]} columns")

            with st.expander("Data Preview", expanded=True):
                st.dataframe(df.head())

            with st.expander("Basic Information"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Rows", df.shape[0])
                col2.metric("Columns", df.shape[1])
                col3.metric("Missing Values", df.isnull().sum().sum())

                st.write("Column Types:")
                st.json(df.dtypes.apply(str).to_dict())

            # Data Preprocessing
            st.subheader("Data Preprocessing")
            if st.checkbox("Remove constant columns", False):
                df = preprocess_data(df, remove_constant=True)
            if st.checkbox("Remove highly correlated columns", False):
                df = preprocess_data(df, remove_correlated=True)
            st.session_state.df = df
            st.session_state.preprocessed_df = df  # Set preprocessed_df to df initially or after preprocessing
            st.session_state.pipeline_status["Preprocessing"] = True
            st.success("Data preprocessing complete!")

            # Run full pipeline steps sequentially
            dataset_name = uploaded_file.name.rsplit('.', 1)[0]
            save_path = f"reports/{dataset_name}"
            insight_report_path = f"{save_path}/insight_report.md"
            model_report_path = f"{save_path}/model_report.md"
            eda_summary_path = f"{save_path}/eda_report.md"
            model_dir = "models"

            st.info("Running Exploratory Data Analysis (EDA)...")
            run_eda(df, save_path=save_path)
            st.session_state.pipeline_status["EDA"] = True
            st.success("EDA completed.")

            st.info("Running Insight Extraction...")
            run_insight_extraction_local(df, output_path=insight_report_path)
            st.session_state.pipeline_status["Insight Extraction"] = True
            st.success("Insight Extraction completed.")

            st.info("Running Modeling...")
            run_modeling(df, output_dir=save_path, model_dir=model_dir)
            st.session_state.pipeline_status["Modeling"] = True
            st.success("Modeling completed.")

            st.info("Generating Report...")
            step1_metadata = {"info": "Metadata from preprocessing step"}
            generate_report(
                dataset_name=dataset_name,
                step1_metadata=step1_metadata,
                eda_summary_path=eda_summary_path,
                insight_report_path=insight_report_path,
                model_report_path=model_report_path,
                output_dir=save_path,
                output_formats=["md", "pdf"]
            )
            st.session_state.pipeline_status["Report Generation"] = True
            st.success("Report generation completed.")

            # Save state after pipeline completion
            save_state(st.session_state.df, st.session_state.pipeline_status, st.session_state.file_name)

            # Display pipeline status panel
            st.subheader("Pipeline Execution Status")
            for step, done in st.session_state.pipeline_status.items():
                status_icon = "✅" if done else "❌"
                st.write(f"{status_icon} {step}")

            # Provide download options using temp storage
            st.subheader("📥 Download Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Download entire report directory as zip
                if os.path.exists(save_path):
                    download_visualizations(save_path, f"{dataset_name}_full_reports")
                else:
                    st.info("Reports not available")
            
            with col2:
                # Download PDF report
                report_pdf_path = f"{save_path}/{dataset_name}_full_report.pdf"
                if os.path.exists(report_pdf_path):
                    download_report(report_pdf_path, "PDF Report")
                else:
                    st.info("PDF report not available")
            
            with col3:
                # Download HTML report
                report_html_path = f"{save_path}/{dataset_name}_styled_report.html"
                if os.path.exists(report_html_path):
                    download_report(report_html_path, "HTML Report")
                else:
                    st.info("HTML report not available")

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

    elif 'df' in st.session_state and st.session_state.df is not None:
        st.info("Using previously uploaded dataset")
        df = st.session_state.df
        st.dataframe(df.head())

        st.subheader("Basic Information")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

        st.write("Column Types:")
        st.json(df.dtypes.apply(str).to_dict())

        if 'pipeline_status' in st.session_state:
            st.subheader("Pipeline Execution Status")
            for step, done in st.session_state.pipeline_status.items():
                status_icon = "✅" if done else "❌"
                st.write(f"{status_icon} {step}")

    else:
        st.info("Please upload a dataset to get started")
