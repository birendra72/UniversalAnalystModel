import streamlit as st
import os
from UAM import data_loader

def show_data_upload():
    st.title("Data Ingestion")
    uploaded_file = st.file_uploader(
        "Upload Dataset (CSV, Excel)", 
        type=["csv", "xlsx"]
    )
    
    if uploaded_file:
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
        st.write(f"Uploaded file: {file_details['filename']} ({file_details['filetype']}, {file_details['filesize']} bytes)")
        
        # Save uploaded file temporarily
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Determine source_type based on extension
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext == 'csv':
            source_type = 'csv'
        elif ext == 'xlsx':
            source_type = 'xlsx'
        else:
            st.error("Unsupported file type")
            return
        
        with st.spinner("Loading data..."):
            df = data_loader.load_data(source_type, {'filepath': temp_file_path})
            st.session_state.df = df
        
        st.success("Data loaded successfully!")
        st.dataframe(df.head())
        
        # Preprocessing options
        if st.checkbox("Show Preprocessing Options"):
            corr_threshold = st.slider("Correlation Threshold to Remove Redundant Features", 0.7, 1.0, 0.95)
            missing_threshold = st.slider("Missing Value Threshold to Drop Columns", 0.0, 1.0, 0.6)
            pca_variance = st.slider("PCA Variance to Keep", 0.5, 1.0, 0.95)
            
            with st.spinner("Preprocessing data..."):
                df_processed, metadata, pca_fig = data_loader.preprocess_data(
                    df, 
                    corr_threshold=corr_threshold, 
                    missing_threshold=missing_threshold, 
                    pca_variance=pca_variance
                )
                st.session_state.preprocessed_df = df_processed
                st.session_state.metadata = metadata
                
                st.success("Preprocessing complete!")
                st.write("Processed Data Preview:")
                st.dataframe(df_processed.head())
                
                if pca_fig:
                    st.pyplot(pca_fig)
