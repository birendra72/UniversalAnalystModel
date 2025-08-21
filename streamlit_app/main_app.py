import streamlit as st
from streamlit_option_menu import option_menu
import data_upload_app as data_upload
import eda_app as eda
import nl_query
import report_app as reports
import modeling_app as modeling
import base64

from streamlit_app import dashboard

# Set page configuration
st.set_page_config(
    page_title="Universal Analyst Model",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base64 encoded background image
background_image = """
iVBORw0KGgoAAAANSUhEUgAAAAMAAAADCAYAAABWKLW/AAAAEklEQVR42mP8//8/AzFixAgGABlDAZ2sHf7qAAAAAElFTkSuQmCC
"""

# Custom CSS for professional styling
def load_css():
    st.markdown(f"""
    <style>
        /* Main styles */
        .stApp {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Header styles */
        .header {{
            display: flex;
            align-items: center;
            padding: 15px 0;
            margin-bottom: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            padding: 15px 25px;
        }}
        
        /* Navigation sidebar */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #2c3e50 0%, #1a2530 100%);
            border-right: none;
            padding: 20px 15px;
        }}
        
        .sidebar-title {{
            color: white !important;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        /* Button styles */
        .stButton>button {{
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%) !important;
            color: white !important;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
            border: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(67, 97, 238, 0.3);
        }}
        
        /* Input styles */
        .stTextInput>div>div>input, 
        .stSelectbox>div>div>div,
        .stTextArea>div>div>textarea {{
            border-radius: 10px;
            padding: 12px 15px;
            border: 1px solid #dee2e6;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
        }}
        
        /* Card styles */
        .metric-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.05);
            margin-bottom: 25px;
            border-left: 4px solid #4361ee;
            transition: all 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}
        
        /* Tab styles */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: white !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            margin: 0 5px !important;
            border: none !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%) !important;
            color: white !important;
        }}
        
        /* Dashboard specific */
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }}
        
        .dashboard-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.05);
            height: 100%;
        }}
        
        .card-title {{
            font-size: 18px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .card-icon {{
            background: #4361ee;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            color: #4361ee;
            margin: 15px 0;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #6c757d;
        }}
        
        /* Status indicators */
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        
        .status-active {{
            background-color: #28a745;
        }}
        
        .status-inactive {{
            background-color: #6c757d;
        }}
        
        /* Footer */
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            color: #6c757d;
            font-size: 14px;
            text-align: center;
        }}
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {{
            .stApp {{
                background: linear-gradient(135deg, #121212 0%, #1e1e1e 100%);
            }}
            
            .header, .metric-card, .dashboard-card {{
                background: #2d2d2d;
                color: #f1f1f1;
            }}
            
            .card-title, .stat-value {{
                color: #f1f1f1;
            }}
            
            .stat-label {{
                color: #a0a0a0;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

# Main application
def main():
    if "preprocessed_df" not in st.session_state:
        st.session_state.preprocessed_df = None

    load_css()
    
    # Custom header with gradient
    st.markdown("""
    <div class="header">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%); 
                        width: 50px; height: 50px; border-radius: 12px; 
                        display: flex; align-items: center; justify-content: center;">
                <span style="color: white; font-size: 24px;">🌐</span>
            </div>
            <div>
                <h1 style="margin:0; color: #2c3e50;">Universal Analyst Model</h1>
                <p style="margin:0; color: #6c757d;">Automated Insights for Data-Driven Decisions</p>
            </div>
        </div>
        <div style="margin-left:auto; display:flex; align-items:center; gap: 20px;">
            <div style="display: flex; align-items: center;">
                <span class="status-indicator status-active"></span>
                <span style="color: #6c757d;">Online</span>
            </div>
            <div style="background: #e9ecef; padding: 8px 15px; border-radius: 50px; 
                        display: flex; align-items: center; gap: 8px;">
                <span style="color: #4361ee;">v1.2</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🌐 UAM NAVIGATION</div>', unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Data Upload", "EDA", "NL Query", "Modeling", "Reports"],
            icons=["speedometer", "cloud-upload", "bar-chart", "chat", "cpu", "file-text"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "white", "font-size": "18px"}, 
                "nav-link": {
                    "font-size": "16px", 
                    "text-align": "left", 
                    "margin": "8px 0", 
                    "border-radius": "8px",
                    "color": "white",
                    "padding": "10px 15px"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%)",
                    "font-weight": "normal",
                },
            }
        )
        
        # Add search bar at the bottom
        st.markdown("---")
        st.markdown("""
        <div style="padding: 15px 10px 5px;">
            <input type="text" placeholder="Type here to search..." 
                style="width: 100%; padding: 10px; border-radius: 8px; 
                border: none; background: rgba(255,255,255,0.1); color: white;">
        </div>
        """, unsafe_allow_html=True)
        
        # Add date/time at the bottom
        st.markdown("""
        <div style="color: rgba(255,255,255,0.6); font-size: 12px; 
                    text-align: center; padding: 10px;">
            <span id="live-time"></span><br>
            <span id="live-date"></span>
        </div>
        <script>
            function updateTime() {
                const now = new Date();
                const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit' };
                const dateOptions = { year: 'numeric', month: '2-digit', day: '2-digit' };
                document.getElementById('live-time').textContent = now.toLocaleTimeString([], timeOptions);
                document.getElementById('live-date').textContent = now.toLocaleDateString([], dateOptions);
            }
            setInterval(updateTime, 1000);
            updateTime();
        </script>
        """, unsafe_allow_html=True)
    
    # Page routing
    if selected == "Dashboard":
        dashboard.show()
    elif selected == "Data Upload":
        data_upload.show()
    elif selected == "EDA":
        eda.show_eda()
    elif selected == "NL Query":
        nl_query.show_nl_query()
    elif selected == "Modeling":
        modeling.show()
    elif selected == "Reports":
        reports.show_report()

if __name__ == "__main__":
    main()