import streamlit as st
import time
import os
import subprocess
import threading
from datetime import datetime
import streamlit.components.v1 as components
from constants import RTMP_URL

# Page configuration
st.set_page_config(
    page_title="YouTube Live Stream Manager",
    page_icon="📺",
    layout="wide"
)

# Session state initialization
if "streaming" not in st.session_state:
    st.session_state.streaming = False
if "ffmpeg_thread" not in st.session_state:
    st.session_state.ffmpeg_thread = None

# Header
st.title("YouTube Live Stream Manager")

# Video upload and stream settings
video_files = [f for f in os.listdir('.') if f.endswith(('.mp4', '.flv'))]

st.write("Available Videos:")
selected_video = st.selectbox("Select video", video_files) if video_files else None

uploaded_file = st.file_uploader("Or upload new video (mp4/flv)", type=['mp4', 'flv'])

if uploaded_file:
    # Save uploaded file
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("Video uploaded successfully!")
    video_path = uploaded_file.name
elif selected_video:
    video_path = selected_video
else:
    video_path = None

# Stream settings
stream_key = st.text_input("Stream Key", type="password")
is_loop = st.checkbox("Enable Loop", value=True)
is_shorts = st.checkbox("Shorts Mode (720x1280)")

# Log display
log_placeholder = st.empty()
logs = []

def log_callback(msg):
    logs.append(msg)
    try:
        log_placeholder.text("\n".join(logs[-20:]))
    except:
        print(msg)

def run_ffmpeg(video_path, stream_key, is_shorts, is_loop, log_callback):
    output_url = f"{RTMP_URL}/{stream_key}"
    scale = "-vf scale=720:1280" if is_shorts else ""
    loop = "-stream_loop" if is_loop else "-stream_loop 0"
    
    cmd = [
        "ffmpeg", "-re", loop, "-1", "-i", video_path,
        "-c:v", "libx264", "-preset", "veryfast", "-b:v", "2500k",
        "-maxrate", "2500k", "-bufsize", "5000k",
        "-g", "60", "-keyint_min", "60",
        "-c:a", "aac", "-b:a", "128k",
        "-f", "flv"
    ]
    
    if scale:
        cmd += scale.split()
    cmd.append(output_url)
    
    log_callback(f"Running command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        for line in process.stdout:
            log_callback(line.strip())
        process.wait()
    except Exception as e:
        log_callback(f"Error: {e}")
    finally:
        log_callback("Stream ended or stopped.")

# Stream controls
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Streaming", type="primary", use_container_width=True):
        if not video_path or not stream_key:
            st.error("Video and stream key are required!")
        else:
            st.session_state.streaming = True
            st.session_state.ffmpeg_thread = threading.Thread(
                target=run_ffmpeg,
                args=(video_path, stream_key, is_shorts, is_loop, log_callback),
                daemon=True
            )
            st.session_state.ffmpeg_thread.start()
            st.success("Stream started!")

with col2:
    if st.button("Stop Streaming", type="primary", use_container_width=True):
        st.session_state.streaming = False
        os.system("pkill ffmpeg")
        st.warning("Stream stopped!")

# Display logs
log_placeholder.text("\n".join(logs[-20:]))

# Stream status
if st.session_state.streaming:
    st.markdown(
        """
        <div style='background-color: #FF0000; color: white; padding: 10px; border-radius: 5px; text-align: center;'>
            🔴 LIVE
        </div>
        """,
        unsafe_allow_html=True
    )
