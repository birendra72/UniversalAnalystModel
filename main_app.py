import streamlit as st
from UAM import data_loader, eda_engine, insight_extractor, nl_query_interface, modeling, report_generator
import data_upload_app
import eda_app
import nl_query
import modeling_app
import report_app

st.set_page_config(
    page_title="Universal Analyst Model",
    page_icon="🌐",
    layout="wide"
)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'preprocessed_df' not in st.session_state:
    st.session_state.preprocessed_df = None
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'report' not in st.session_state:
    st.session_state.report = None

# Sidebar navigation
st.sidebar.title("🌐 Universal Analyst")
app_mode = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Data Upload", "EDA", "Insights", "NL Query", "Modeling", "Report"]
)

if app_mode == "Home":
    st.title("Universal Analyst Model")
    st.image("assets/dashboard_preview.png", use_column_width=True)
    st.markdown("### Automated Data Analysis for Everyone")
    st.write("Upload your dataset and get instant insights, visualizations, and predictive models.")

elif app_mode == "Data Upload":
    data_upload_app.show_data_upload()

elif app_mode == "EDA":
    eda_app.show_eda()

elif app_mode == "Insights":
    st.title("Insights")
    if st.session_state.preprocessed_df is None:
        st.warning("Please upload and preprocess data first!")
    else:
        insights = insight_extractor.run_insight_extraction(st.session_state.preprocessed_df)
        if insights is not None:
            try:
                for insight in insights:
                    st.write(f"- {insight}")
            except TypeError:
                st.write(insights)  # If insights is not iterable, just write it
        else:
            st.warning("No insights found. Please ensure your data is preprocessed correctly.")
elif app_mode == "NL Query":
    nl_query.show_nl_query()

elif app_mode == "Modeling":
    modeling_app.show()

elif app_mode == "Report":
    report_app.show_report()
