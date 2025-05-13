import streamlit as st
from constants import RTMP_URL, SUPPORTED_VIDEO_FORMATS, MAX_VIDEO_SIZE
from streamlit_utils import validate_video_file, save_uploaded_video

def render_stream_setup(rtmp_url):
    """Render the stream setup tab content"""
    
    st.header("Stream Setup")
    
    # Video upload section
    with st.container(border=True):
        st.markdown("### Video Source")
        source_type = st.radio(
            "Select video source",
            options=["Upload Video", "Stream Key"],
            horizontal=True
        )
        
        if source_type == "Upload Video":
            st.markdown(f"""
                Supported formats: {", ".join(SUPPORTED_VIDEO_FORMATS)}  
                Maximum file size: {MAX_VIDEO_SIZE // (1024 * 1024)}MB
            """)
            
            uploaded_file = st.file_uploader(
                "Choose a video file",
                type=SUPPORTED_VIDEO_FORMATS,
                help="Upload a video file to stream"
            )
            
            if uploaded_file:
                is_valid, message = validate_video_file(uploaded_file)
                if is_valid:
                    # Video preview
                    st.video(uploaded_file)
                    
                    # Loop settings
                    col1, col2 = st.columns(2)
                    with col1:
                        loop_enabled = st.checkbox("Enable loop", value=True)
                    with col2:
                        if loop_enabled:
                            smooth_loop = st.checkbox(
                                "Smooth loop transition",
                                value=True,
                                help="Adds a subtle fade transition between loops"
                            )
                    
                    # Save video settings to session state
                    st.session_state.video_settings = {
                        "file_path": save_uploaded_video(uploaded_file),
                        "loop_enabled": loop_enabled,
                        "smooth_loop": smooth_loop if loop_enabled else False
                    }
                else:
                    st.error(message)
        else:
            # Stream key input with toggle for visibility
            st.markdown(
                """
                ### Stream Key Configuration
                Enter your YouTube stream key below. Your stream key is sensitive information - never share it publicly.
                
                **RTMP URL:** `rtmp://a.rtmp.youtube.com/live2`
                """,
            )
            
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
