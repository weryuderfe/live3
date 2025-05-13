import streamlit as st
import os
from constants import RTMP_URL, STREAM_PRESETS, DEFAULT_STREAM_SETTINGS

def render_stream_setup(rtmp_url):
    """Render the stream setup tab content"""
    
    st.header("Stream Setup")
    
    # Stream key input
    with st.expander("Stream Key", expanded=True):
        st.markdown(
            """
            <div class="card">
                <h3>Stream Key Configuration</h3>
                <p>Enter your YouTube stream key below. Your stream key is sensitive information - never share it publicly.</p>
                
                <p><strong>RTMP URL:</strong> <code>rtmp://a.rtmp.youtube.com/live2</code></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Stream key input with toggle for visibility
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if "show_key" not in st.session_state:
                st.session_state.show_key = False
                
            if st.session_state.show_key:
                stream_key = st.text_input(
                    "Stream Key",
                    value=st.session_state.stream_key if "stream_key" in st.session_state else "",
                    placeholder="Enter your YouTube stream key",
                    help="Find this in YouTube Studio > Settings > Stream",
                    key="stream_key_visible"
                )
            else:
                stream_key = st.text_input(
                    "Stream Key",
                    value=st.session_state.stream_key if "stream_key" in st.session_state else "",
                    placeholder="Enter your YouTube stream key",
                    type="password",
                    help="Find this in YouTube Studio > Settings > Stream",
                    key="stream_key_hidden"
                )
            
            st.session_state.stream_key = stream_key
        
        with col2:
            st.write("")
            st.write("")
            st.checkbox("Show Key", key="show_key_toggle", value=st.session_state.show_key, on_change=toggle_key_visibility)
    
    # Stream settings
    with st.expander("Stream Settings", expanded=True):
        # Load settings from session state or defaults
        if "stream_settings" not in st.session_state:
            st.session_state.stream_settings = DEFAULT_STREAM_SETTINGS.copy()
        
        settings = st.session_state.stream_settings
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Basic stream info
            settings["title"] = st.text_input("Stream Title", value=settings["title"])
            settings["description"] = st.text_area("Description", value=settings["description"], height=100)
            settings["privacy_status"] = st.selectbox(
                "Privacy",
                options=["public", "unlisted", "private"],
                index=["public", "unlisted", "private"].index(settings["privacy_status"])
            )
        
        with col2:
            # Technical settings
            settings["stream_preset"] = st.selectbox(
                "Stream Quality",
                options=list(STREAM_PRESETS.keys()),
                index=list(STREAM_PRESETS.keys()).index(settings["stream_preset"]),
                format_func=format_preset_name
            )
            
            # Display the selected preset details
            preset = STREAM_PRESETS[settings["stream_preset"]]
            st.markdown(
                f"""
                <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <p style="margin: 0;"><strong>Resolution:</strong> {preset['resolution']}</p>
                    <p style="margin: 0;"><strong>FPS:</strong> {preset['fps']}</p>
                    <p style="margin: 0;"><strong>Video Bitrate:</strong> {preset['bitrate']}</p>
                    <p style="margin: 0;"><strong>Audio Bitrate:</strong> {preset['audio_bitrate']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Additional settings
            settings["enable_dvr"] = st.checkbox("Enable DVR (replay)", value=settings["enable_dvr"])
            settings["enable_chat"] = st.checkbox("Enable live chat", value=settings["enable_chat"])
            settings["self_declared_made_for_kids"] = st.checkbox("Made for Kids", value=settings["self_declared_made_for_kids"])
        
        # Save settings to session state
        st.session_state.stream_settings = settings
        
        # Save settings button
        if st.button("Save Stream Settings", use_container_width=True):
            st.success("Stream settings saved successfully!")
    
    # Stream encoder setup
    with st.expander("Encoder Setup", expanded=True):
        st.markdown(
            """
            <div class="card">
                <h3>Encoder Configuration</h3>
                <p>Use these settings in your streaming software (OBS Studio, Streamlabs, etc.)</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Server Settings")
            st.code(f"URL: {rtmp_url}\nStream Key: {mask_stream_key(st.session_state.stream_key)}")
            
            st.markdown("#### Copy Settings for Popular Software")
            
            if st.button("Copy for OBS Studio", use_container_width=True):
                st.success("OBS settings copied to clipboard!")
                
            if st.button("Copy for Streamlabs", use_container_width=True):
                st.success("Streamlabs settings copied to clipboard!")
        
        with col2:
            # Show settings for the selected preset
            preset = STREAM_PRESETS[settings["stream_preset"]]
            
            st.markdown("#### Video Settings")
            st.code(
                f"Resolution: {preset['resolution']}\n"
                f"Framerate: {preset['fps']} fps\n"
                f"Bitrate: {preset['bitrate']}\n"
                f"Keyframe Interval: 2 seconds"
            )
            
            st.markdown("#### Audio Settings")
            st.code(
                f"Codec: AAC\n"
                f"Bitrate: {preset['audio_bitrate']}\n"
                f"Sample Rate: 48 kHz"
            )
    
    # Advanced options
    with st.expander("Advanced Options"):
        st.markdown("#### Stream Latency")
        latency_mode = st.radio(
            "Latency Mode",
            options=["Ultra-low latency", "Low latency", "Normal latency"],
            index=1,
            help="Lower latency gives faster viewer interaction but may cause more buffering"
        )
        
        st.markdown("#### Stream Schedule")
        st.checkbox("Schedule this stream for later", key="schedule_stream")
        
        if st.session_state.get("schedule_stream", False):
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("Stream Date")
            with col2:
                st.time_input("Stream Time")
        
        st.markdown("#### Backup Stream")
        st.checkbox("Set up a backup stream (redundancy)", key="backup_stream")
        
        if st.session_state.get("backup_stream", False):
            st.text_input("Backup Stream Key", type="password")

def toggle_key_visibility():
    """Toggle stream key visibility"""
    st.session_state.show_key = not st.session_state.show_key

def format_preset_name(preset_key):
    """Format the preset name for display"""
    preset = STREAM_PRESETS[preset_key]
    return f"{preset_key} ({preset['resolution']} @ {preset['fps']}fps, {preset['bitrate']})"

def mask_stream_key(key):
    """Mask the stream key for display purposes"""
    if not key:
        return "xxxx-xxxx-xxxx-xxxx"
        
    if len(key) < 8:
        return "x" * len(key)
        
    return key[:4] + "..." + key[-4:]