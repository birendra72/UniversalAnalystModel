import streamlit as st
import pandas as pd
from UAM import nl_query_interface

def show_nl_query():
    st.title("Natural Language Query")
    st.info("Ask questions about your data in plain English")
    
    if st.session_state.preprocessed_df is None:
        st.warning("Please upload and preprocess data first!")
        return
    
    query = st.text_input("Ask a question about your data:")
    api_key = st.text_input("OpenAI API Key:", type="password")
    
    if st.button("Submit Query") and api_key and query:
        with st.spinner("Processing your question..."):
            try:
                nlq = nl_query_interface.NaturalLanguageQueryInterface(
                    st.session_state.preprocessed_df,
                    openai_api_key=api_key
                )
                result = nlq.ask(query)
                if isinstance(result, pd.DataFrame):
                    st.dataframe(result)
                    csv = result.to_csv(index=False)
                    st.download_button("Export as CSV", csv, "query_result.csv")
                else:
                    st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
