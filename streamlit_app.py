import streamlit as st
import os
import json
import time
from datetime import datetime
import plotly.graph_objects as go
from streamlit_utils import (
    authenticate_youtube,
    get_stream_health,
    get_stream_analytics,
    start_stream,
    stop_stream,
    get_live_chat_messages,
    send_chat_message,
)
from style_utils import apply_custom_styles, main_page_config
from components.stream_setup import render_stream_setup
from components.stream_monitor import render_stream_monitor
from components.chat_manager import render_chat_manager
from components.analytics_dashboard import render_analytics_dashboard
from constants import RTMP_URL

# Page configuration
apply_custom_styles()
main_page_config("YouTube Live Stream Manager")

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "streaming" not in st.session_state:
    st.session_state.streaming = False
if "stream_start_time" not in st.session_state:
    st.session_state.stream_start_time = None
if "stream_key" not in st.session_state:
    st.session_state.stream_key = ""
if "stream_health" not in st.session_state:
    st.session_state.stream_health = {"status": "offline", "health": 0, "viewers": 0}
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "Setup"

# Header with YouTube branding
st.markdown(
    """
    <div class="header">
        <h1>
            <span style="color: #FF0000;">YouTube</span> Live Stream Manager
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Authentication section
if not st.session_state.authenticated:
    st.info("Please authenticate with YouTube to manage your live streams")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://www.gstatic.com/youtube/img/branding/youtubelogo/svg/youtubelogo.svg", width=150)
    with col2:
        if st.button("Authenticate with YouTube", key="auth_button", use_container_width=True):
            with st.spinner("Authenticating..."):
                success = authenticate_youtube()
                if success:
                    st.session_state.authenticated = True
                    st.experimental_rerun()
                else:
                    st.error("Authentication failed. Please try again.")
else:
    # Main navigation
    tabs = ["Setup", "Monitor", "Chat", "Analytics"]
    cols = st.columns(len(tabs))
    
    for i, tab in enumerate(tabs):
        with cols[i]:
            if st.button(
                tab, 
                use_container_width=True,
                type="primary" if st.session_state.selected_tab == tab else "secondary"
            ):
                st.session_state.selected_tab = tab
                st.experimental_rerun()
    
    st.divider()
    
    # Main content based on selected tab
    if st.session_state.selected_tab == "Setup":
        render_stream_setup(RTMP_URL)
    
    elif st.session_state.selected_tab == "Monitor":
        render_stream_monitor()
    
    elif st.session_state.selected_tab == "Chat":
        render_chat_manager()
    
    elif st.session_state.selected_tab == "Analytics":
        render_analytics_dashboard()
    
    # Stream control buttons (fixed at bottom)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if not st.session_state.streaming:
            if st.button("Start Streaming", type="primary", use_container_width=True):
                if st.session_state.stream_key:
                    with st.spinner("Starting stream..."):
                        success = start_stream(st.session_state.stream_key)
                        if success:
                            st.session_state.streaming = True
                            st.session_state.stream_start_time = datetime.now()
                            st.success("Stream started successfully!")
                            time.sleep(1)
                            st.experimental_rerun()
                        else:
                            st.error("Failed to start stream. Check your stream key and try again.")
                else:
                    st.warning("Please enter your stream key in the Setup tab first.")
        else:
            if st.button("Stop Streaming", type="primary", use_container_width=True):
                with st.spinner("Stopping stream..."):
                    success = stop_stream()
                    if success:
                        st.session_state.streaming = False
                        st.session_state.stream_start_time = None
                        st.success("Stream stopped successfully!")
                        time.sleep(1)
                        st.experimental_rerun()
                    else:
                        st.error("Failed to stop stream.")
    
    with col2:
        # Stream health indicator
        if st.session_state.streaming:
            stream_health = get_stream_health()
            health_color = "#4CAF50" if stream_health["health"] > 80 else "#FFC107" if stream_health["health"] > 50 else "#F44336"
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <p>Stream Health: <span style="color: {health_color}; font-weight: bold;">{stream_health["status"]}</span></p>
                    <div style="height: 10px; background-color: #e0e0e0; border-radius: 5px;">
                        <div style="width: {stream_health["health"]}%; height: 100%; background-color: {health_color}; border-radius: 5px;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="text-align: center;">
                    <p>Stream Status: <span style="color: gray; font-weight: bold;">Offline</span></p>
                    <div style="height: 10px; background-color: #e0e0e0; border-radius: 5px;"></div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with col3:
        # Stream duration or viewers count
        if st.session_state.streaming and st.session_state.stream_start_time:
            duration = datetime.now() - st.session_state.stream_start_time
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <p>Duration: <span style="font-weight: bold;">{hours:02}:{minutes:02}:{seconds:02}</span></p>
                    <p>Viewers: <span style="font-weight: bold;">{st.session_state.stream_health["viewers"]}</span></p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="text-align: center;">
                    <p>Duration: <span style="color: gray; font-weight: bold;">00:00:00</span></p>
                    <p>Viewers: <span style="color: gray; font-weight: bold;">0</span></p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Footer
    st.markdown(
        """
        <div style="text-align: center; margin-top: 30px; color: #9e9e9e; font-size: 12px;">
            <p>YouTube RTMP Streaming Tool • Built with Streamlit • v0.1.0</p>
            <p>RTMP URL: rtmp://a.rtmp.youtube.com/live2</p>
        </div>
        """,
        unsafe_allow_html=True
    )