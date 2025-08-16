import streamlit as st
from UAM import report_generator
import os
import re
def show_report():
    st.title("Automated Reporting")
    if 'preprocessed_df' not in st.session_state or st.session_state.preprocessed_df is None:
        st.warning("Please upload and preprocess data first!")
        return

    dataset_name = st.session_state.file_name.rsplit('.', 1)[0] if 'file_name' in st.session_state else "general"
    save_path = f"reports/{dataset_name}"
    report_md_path = f"{save_path}/{dataset_name}_full_report.md"
    report_pdf_path = f"{save_path}/{dataset_name}_full_report.pdf"
    report_html_path = f"{save_path}/{dataset_name}_styled_report.html"

    # Show markdown report if exists
    try:
        with open(report_md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        # Fix image paths in markdown to include report folder path
        md_content = re.sub(r'!\[(.*?)\]\((?!http)(.*?)\)', fr'![\1]({save_path}/\2)', md_content)
        st.markdown(md_content, unsafe_allow_html=True)
        st.markdown(md_content)
    except FileNotFoundError:
        st.warning("Markdown report not found. Please run the full pipeline to generate reports.")

    # Provide download button for PDF report
    try:
        with open(report_pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Full Report (PDF)",
                data=pdf_file,
                file_name=f"{dataset_name}_full_report.pdf",
                mime="application/pdf"
            )
    except FileNotFoundError:
        st.warning("PDF report not found. Please run the full pipeline to generate reports.")

    # Provide link to view HTML report
    if os.path.exists(report_html_path):
        st.markdown(f"[View Full Report (HTML)]({report_html_path})")
    else:
        st.warning("HTML report not found. Please run the full pipeline to generate reports.")
