# import streamlit as st
# import os
# import glob
# from utils.cli_interface import run_eda

# def show():
#     st.title("🔍 Exploratory Data Analysis")
    
#     if 'df' not in st.session_state:
#         st.warning("Please upload data first")
#         return
    
#     df = st.session_state.df
    
#     if st.button("Generate EDA Visualizations"):
#         with st.spinner("Creating visualizations..."):
#             output_dir = "eda_outputs"
#             os.makedirs(output_dir, exist_ok=True)
#             run_eda(df, save_path=output_dir)
#             st.session_state.eda_generated = True
#             st.success("EDA visualizations generated!")
    
#     if st.session_state.get('eda_generated', False):
#         st.subheader("Generated Visualizations")
#         images = glob.glob("eda_outputs/*.png")
#         cols = st.columns(3)
#         for i, img_path in enumerate(images):
#             with cols[i % 3]:
#                 st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)
