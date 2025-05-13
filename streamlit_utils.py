import streamlit as st
import time
from datetime import datetime
import os
import tempfile

def get_stream_health():
    """Get the current stream health metrics (mock implementation)"""
    if not st.session_state.streaming:
        return {"status": "offline", "health": 0}
    
    # Simulate random health metrics
    health = 95  # Simplified to always return good health
    status = "Excellent" if health > 90 else "Good"
    
    return {
        "status": status,
        "health": health
    }

def start_stream(stream_key):
    """Start a YouTube live stream (mock implementation)"""
    time.sleep(2)  # Simulate startup time
    return True

def stop_stream():
    """Stop a YouTube live stream (mock implementation)"""
    time.sleep(1)  # Simulate shutdown time
    return True

def save_uploaded_video(uploaded_file):
    """Save uploaded video to temporary directory"""
    if uploaded_file is None:
        return None
        
    # Create temp directory if it doesn't exist
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    
    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def validate_video_file(uploaded_file):
    """Validate uploaded video file"""
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file extension
    file_ext = uploaded_file.name.split(".")[-1].lower()
    if file_ext not in ["mp4", "webm", "mov"]:
        return False, "Unsupported file format. Please upload MP4, WebM, or MOV files."
    
    # Check file size (100MB limit)
    if uploaded_file.size > 100 * 1024 * 1024:
        return False, "File size too large. Maximum size is 100MB."
    
    return True, "File is valid"
