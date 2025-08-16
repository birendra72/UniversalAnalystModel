import streamlit as st
import os
import glob
import hashlib
import pandas as pd
from UAM import eda_engine

def get_dataset_hash(df):
    """Generate a unique hash for the dataset to identify if it's the same data"""
    # Create a string representation of the dataframe structure and content
    data_str = str(df.shape) + str(df.dtypes) + str(df.head(100).values.tobytes())
    return hashlib.md5(data_str.encode()).hexdigest()

def show_eda():
    st.title("Exploratory Data Analysis")
    
    # Use preprocessed_df if available, else fallback to raw df
    df = st.session_state.get("preprocessed_df")
    if df is None:
        df = st.session_state.get("df")
        if df is None:
            st.warning("Please upload data first!")
            return
    
    # Generate dataset hash for caching
    dataset_hash = get_dataset_hash(df)
    cache_dir = f"eda_outputs/{dataset_hash}"
    
    # Check if visualizations already exist
    existing_visualizations = []
    if os.path.exists(cache_dir):
        existing_visualizations = sorted(glob.glob(os.path.join(cache_dir, "*.png")))
    
    # Display cache status
    if existing_visualizations:
        st.info(f"📊 Found {len(existing_visualizations)} existing visualizations. Using cached results.")
        regenerate = st.checkbox("Force regenerate visualizations", value=False)
    else:
        st.info("No cached visualizations found. Will generate new ones.")
        regenerate = True
    
    if st.button("Generate Visualizations"):
        if not regenerate and existing_visualizations:
            st.success("Using cached visualizations!")
        else:
            with st.spinner("Creating visualizations..."):
                # Clean old cache if regenerating
                if regenerate and os.path.exists(cache_dir):
                    for file in glob.glob(os.path.join(cache_dir, "*.png")):
                        os.remove(file)
                
                # Generate new visualizations
                os.makedirs(cache_dir, exist_ok=True)
                eda_engine.generate_eda_visuals(df, cache_dir)
                st.success("EDA visualizations generated!")
    
    # Display visualizations from cache directory
    image_files = sorted(glob.glob(os.path.join(cache_dir, "*.png")))
    if image_files:
        st.subheader("Generated Visualizations")
        for i in range(0, len(image_files), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(image_files):
                    cols[j].image(image_files[i + j], 
                                caption=os.path.basename(image_files[i + j]),
                                use_column_width=True)
    else:
        st.info("No visualizations to display. Click 'Generate Visualizations' to create them.")

if __name__ == "__main__":
    show_eda()
