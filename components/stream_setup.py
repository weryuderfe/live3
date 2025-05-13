import streamlit as st
from constants import RTMP_URL

def render_stream_setup(rtmp_url):
    """Render the stream setup tab content"""
    
    st.header("Stream Setup")
    
    # Stream key input
    with st.container(border=True):
        st.markdown(
            """
            ### Stream Key Configuration
            Enter your YouTube stream key below. Your stream key is sensitive information - never share it publicly.
            
            **RTMP URL:** `rtmp://a.rtmp.youtube.com/live2`
            """,
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
    
    # Encoder setup info
    with st.container(border=True):
        st.markdown("### Encoder Configuration")
        st.markdown("Use these settings in your streaming software (OBS Studio, Streamlabs, etc.)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Server Settings")
            st.code(f"URL: {rtmp_url}\nStream Key: {mask_stream_key(st.session_state.stream_key)}")
        
        with col2:
            st.markdown("#### Recommended Settings")
            st.code(
                "Resolution: 1280x720\n"
                "Framerate: 30 fps\n"
                "Video Bitrate: 3000 kbps\n"
                "Audio Bitrate: 128 kbps\n"
                "Keyframe Interval: 2 seconds"
            )

def toggle_key_visibility():
    """Toggle stream key visibility"""
    st.session_state.show_key = not st.session_state.show_key

def mask_stream_key(key):
    """Mask the stream key for display purposes"""
    if not key:
        return "xxxx-xxxx-xxxx-xxxx"
        
    if len(key) < 8:
        return "x" * len(key)
        
    return key[:4] + "..." + key[-4:]
