import streamlit as st
import os
import json
import time
from datetime import datetime, timedelta
import random

# In a real application, these functions would connect to the YouTube API
# Since we can't actually connect to YouTube, these are mock implementations

def authenticate_youtube():
    """Mock YouTube authentication function"""
    # In a real app, this would open the OAuth flow
    time.sleep(2)  # Simulate network delay
    
    # Return success (in a real app, this would validate the auth response)
    return True

def get_stream_health():
    """Get the current stream health metrics (mock implementation)"""
    # In a real app, this would call the YouTube API
    
    if not st.session_state.streaming:
        return {"status": "offline", "health": 0, "viewers": 0}
    
    # Simulate random health metrics
    health = random.randint(70, 100)
    status = "Excellent" if health > 90 else "Good" if health > 80 else "Fair" if health > 60 else "Poor"
    viewers = random.randint(10, 100)
    
    return {
        "status": status,
        "health": health,
        "viewers": viewers
    }

def get_stream_analytics():
    """Get stream analytics data (mock implementation)"""
    # In a real app, this would call the YouTube Analytics API
    
    if not st.session_state.streaming and not st.session_state.stream_start_time:
        # Generate some demo data if not streaming
        now = datetime.now()
        start_time = now - timedelta(hours=1)
        
        # Create timestamped data points at 5-minute intervals
        times = []
        viewers = []
        likes = []
        
        for i in range(13):  # 1 hour in 5-minute intervals
            timestamp = start_time + timedelta(minutes=5*i)
            times.append(timestamp.strftime("%H:%M"))
            # Generate some realistic looking viewer counts
            view_count = int(25 * (1 + 0.5 * i + random.random() * 0.2))
            viewers.append(view_count)
            # Generate like counts as roughly 10% of viewers
            likes.append(int(view_count * 0.1 * (1 + random.random() * 0.5)))
        
        return {
            "times": times,
            "viewers": viewers,
            "likes": likes,
            "peak_viewers": max(viewers),
            "avg_viewers": sum(viewers) // len(viewers),
            "total_likes": sum(likes),
            "comments": random.randint(100, 300),
        }
    
    # If currently streaming, create realistic data based on stream time
    if st.session_state.streaming and st.session_state.stream_start_time:
        now = datetime.now()
        start_time = st.session_state.stream_start_time
        duration = (now - start_time).total_seconds() / 60  # duration in minutes
        
        # Create data points at 5-minute intervals
        times = []
        viewers = []
        likes = []
        
        # Get the number of 5-minute intervals that have passed
        intervals = max(1, int(duration / 5))
        
        for i in range(intervals + 1):
            timestamp = start_time + timedelta(minutes=5*i)
            if timestamp > now:
                break
                
            times.append(timestamp.strftime("%H:%M"))
            
            # Generate viewer curve that rises and has some fluctuation
            base_viewers = 10
            time_factor = min(2.0, i / 6)  # Increases over time but caps at 2x
            random_factor = random.random() * 0.3 + 0.85  # Random 0.85-1.15
            
            view_count = int(base_viewers * time_factor * random_factor * intervals)
            viewers.append(view_count)
            
            # Likes are roughly 5-15% of viewers
            like_rate = random.random() * 0.1 + 0.05  # 5-15%
            likes.append(int(view_count * like_rate))
        
        return {
            "times": times,
            "viewers": viewers,
            "likes": likes,
            "peak_viewers": max(viewers),
            "avg_viewers": sum(viewers) // len(viewers) if viewers else 0,
            "total_likes": sum(likes),
            "comments": int(sum(viewers) * 0.2),  # About 20% of total viewers leave comments
        }
    
    # Fallback empty data
    return {
        "times": [],
        "viewers": [],
        "likes": [],
        "peak_viewers": 0,
        "avg_viewers": 0,
        "total_likes": 0,
        "comments": 0,
    }

def start_stream(stream_key):
    """Start a YouTube live stream (mock implementation)"""
    # In a real app, this would configure and start FFMPEG with the RTMP URL
    time.sleep(2)  # Simulate startup time
    
    # Update stream health (mock data)
    st.session_state.stream_health = {
        "status": "Good",
        "health": 90,
        "viewers": 0
    }
    
    return True

def stop_stream():
    """Stop a YouTube live stream (mock implementation)"""
    # In a real app, this would stop FFMPEG and close the stream
    time.sleep(1)  # Simulate shutdown time
    
    return True

def get_live_chat_messages():
    """Get live chat messages (mock implementation)"""
    # In a real app, this would pull from the YouTube Live Chat API
    
    if not st.session_state.streaming:
        return []
    
    # Sample viewer names
    viewer_names = ["YouTubeFan123", "StreamViewer", "ContentLover", "LiveChatUser", 
                   "TechEnthusiast", "GamingPro", "MusicLover", "ArtFan"]
    
    # Sample message content
    message_templates = [
        "Hey everyone! Loving the stream!",
        "First time here, this is great!",
        "Can you talk about {topic}?",
        "Hello from {location}!",
        "Great content as always!",
        "Just subscribed!",
        "What software are you using?",
        "The quality looks amazing today!",
        "👍 👍 👍",
        "Will this be available as a VOD later?",
    ]
    
    topics = ["YouTube algorithm", "streaming setup", "content creation", "your equipment", "your schedule"]
    locations = ["California", "New York", "London", "Tokyo", "Australia", "Canada", "Germany", "Brazil"]
    
    # Generate 3-8 random messages
    num_messages = random.randint(3, 8)
    messages = []
    
    now = datetime.now()
    
    for i in range(num_messages):
        # Create a message in the past 5 minutes
        timestamp = now - timedelta(minutes=random.randint(0, 5), seconds=random.randint(0, 59))
        
        # Select and format a random message template
        msg_template = random.choice(message_templates)
        if "{topic}" in msg_template:
            msg_template = msg_template.replace("{topic}", random.choice(topics))
        if "{location}" in msg_template:
            msg_template = msg_template.replace("{location}", random.choice(locations))
        
        # Determine if this should be a special message type
        message_type = "regular"
        if random.random() < 0.1:  # 10% chance of special message
            message_type = random.choice(["super_chat", "membership"])
        
        messages.append({
            "id": f"msg_{int(time.time())}_{i}",
            "author": random.choice(viewer_names),
            "message": msg_template,
            "timestamp": timestamp.strftime("%H:%M:%S"),
            "type": message_type,
            "amount": "$5.00" if message_type == "super_chat" else None
        })
    
    return sorted(messages, key=lambda x: x["timestamp"])

def send_chat_message(message):
    """Send a chat message as the stream owner (mock implementation)"""
    # In a real app, this would post to the YouTube Live Chat API
    time.sleep(0.5)  # Simulate network delay
    
    return True