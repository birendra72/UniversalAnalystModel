import streamlit as st
from UAM import report_generator
import os
import re
import glob
import streamlit.components.v1 as components
from streamlit_app.utils.temp_storage import temp_storage, download_report, download_visualizations

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

    # Enhanced download section at the top
    if os.path.exists(save_path):
        st.markdown("---")
        st.subheader("📦 Download Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download entire report directory as zip
            download_visualizations(save_path, f"{dataset_name}_full_reports")
        
        with col2:
            # Download individual PDF report if exists
            if os.path.exists(report_pdf_path):
                download_report(report_pdf_path, "PDF Report")
            else:
                st.info("PDF report not available")
        
        with col3:
            # Download individual HTML report if exists
            if os.path.exists(report_html_path):
                download_report(report_html_path, "HTML Report")
            else:
                st.info("HTML report not available")
        
        st.markdown("---")

    # Show HTML report if exists (preferred approach)
    if os.path.exists(report_html_path):
        st.success("Report loaded successfully!")
        
        # Read and display the HTML report
        with open(report_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Display the HTML content
        components.html(html_content, height=800, scrolling=True)
        
        # Enhanced download options below the report
        st.markdown("---")
        st.subheader("📥 Download Individual Files")
        
        cols = st.columns(3)
        
        with cols[0]:
            # Download PDF
            if os.path.exists(report_pdf_path):
                download_report(report_pdf_path, "PDF")
            else:
                st.info("PDF not available")
        
        with cols[1]:
            # Download HTML
            if os.path.exists(report_html_path):
                download_report(report_html_path, "HTML")
            else:
                st.info("HTML not available")
        
        with cols[2]:
            # Download Markdown
            if os.path.exists(report_md_path):
                download_report(report_md_path, "Markdown")
            else:
                st.info("Markdown not available")
    
    # Fallback to markdown if HTML doesn't exist
    elif os.path.exists(report_md_path):
        st.info("HTML report not found, displaying markdown version...")
        
        with open(report_md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Process the markdown content to handle images
        lines = md_content.split('\n')
        processed_lines = []
        
        for line in lines:
            # Check if this line contains an image
            image_match = re.match(r'!\[(.*?)\]\(([^)]+)\)', line.strip())
            if image_match:
                alt_text = image_match.group(1)
                image_path = image_match.group(2)
                
                # Skip if it's already an absolute path or URL
                if not image_path.startswith(('http://', 'https://', '/')):
                    # Convert relative path to absolute path
                    full_image_path = os.path.join(save_path, image_path)
                    
                    # Check if the image exists
                    if os.path.exists(full_image_path):
                        # Display the image using st.image
                        st.image(full_image_path, caption=alt_text or "Visualization")
                        continue
            
            # Add the line to processed content
            processed_lines.append(line)
        
        # Display the remaining markdown content
        remaining_content = '\n'.join(processed_lines)
        st.markdown(remaining_content, unsafe_allow_html=True)
        
        # Enhanced download options
        st.markdown("---")
        st.subheader("📥 Download Options")
        
        cols = st.columns(2)
        
        with cols[0]:
            # Download PDF report
            if os.path.exists(report_pdf_path):
                download_report(report_pdf_path, "PDF Report")
            else:
                st.info("PDF report not available")
        
        with cols[1]:
            # Download Markdown report
            if os.path.exists(report_md_path):
                download_report(report_md_path, "Markdown Report")
            else:
                st.info("Markdown report not available")
    
    else:
        st.warning("No reports found. Please run the full pipeline to generate reports.")
