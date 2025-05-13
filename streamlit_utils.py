import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app"""
    
    st.markdown(
        """
        <style>
            /* Main container styles */
            .stApp {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            /* Header styles */
            .header {
                text-align: center;
                margin-bottom: 2rem;
            }
            
            /* Card container styles */
            .card {
                background-color: white;
                border-radius: 8px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }
            
            /* Metric card styles */
            .metric-card {
                text-align: center;
                padding: 1rem;
                background: white;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }
            
            .metric-card h3 {
                margin: 0;
                font-size: 0.9rem;
                color: #666;
            }
            
            .metric-card p {
                margin: 0.5rem 0 0 0;
                font-size: 1.5rem;
                font-weight: bold;
            }
            
            /* Button styles */
            .stButton > button {
                width: 100%;
                border-radius: 4px;
                padding: 0.5rem 1rem;
                font-weight: 500;
            }
            
            /* Status indicator styles */
            .status-indicator {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-right: 6px;
            }
            
            .status-online {
                background-color: #4CAF50;
            }
            
            .status-offline {
                background-color: #9e9e9e;
            }
            
            /* Stream health bar styles */
            .health-bar {
                width: 100%;
                height: 8px;
                background-color: #e0e0e0;
                border-radius: 4px;
                overflow: hidden;
            }
            
            .health-bar-fill {
                height: 100%;
                border-radius: 4px;
                transition: width 0.3s ease;
            }
            
            /* Chat message styles */
            .chat-message {
                padding: 0.5rem 1rem;
                margin-bottom: 0.5rem;
                border-radius: 4px;
                background-color: #f5f5f5;
            }
            
            .chat-message.owner {
                background-color: #e3f2fd;
            }
            
            .chat-message.super-chat {
                background-color: #ffebee;
            }
            
            /* Analytics chart styles */
            .chart-container {
                background: white;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }
            
            /* Form field styles */
            .stTextInput > div > div > input {
                border-radius: 4px;
            }
            
            .stSelectbox > div > div > select {
                border-radius: 4px;
            }
            
            /* Tab styles */
            .stTabs {
                background: white;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def main_page_config(title):
    """Configure the main page settings"""
    
    st.set_page_config(
        page_title=title,
        page_icon="📺",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
