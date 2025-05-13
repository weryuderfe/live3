# YouTube RTMP streaming configuration
RTMP_URL = "rtmp://a.rtmp.youtube.com/live2"

# Stream quality presets
STREAM_PRESETS = {
    "720p30": {
        "resolution": "1280x720",
        "fps": 30,
        "bitrate": "3000k",
        "audio_bitrate": "128k"
    },
    "720p60": {
        "resolution": "1280x720",
        "fps": 60,
        "bitrate": "4500k",
        "audio_bitrate": "128k"
    },
    "1080p30": {
        "resolution": "1920x1080",
        "fps": 30,
        "bitrate": "6000k",
        "audio_bitrate": "128k"
    },
    "1080p60": {
        "resolution": "1920x1080",
        "fps": 60,
        "bitrate": "9000k",
        "audio_bitrate": "128k"
    }
}

# YouTube API scopes required for streaming
YOUTUBE_API_SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

# Chat message types
CHAT_MESSAGE_TYPES = {
    "regular": "Regular message",
    "super_chat": "Super Chat",
    "super_sticker": "Super Sticker",
    "membership": "New/Renewed Membership",
}

# Moderation actions
MODERATION_ACTIONS = {
    "timeout": "Timeout User",
    "hide": "Hide Message",
    "block": "Block User",
    "report": "Report User"
}

# Default stream settings
DEFAULT_STREAM_SETTINGS = {
    "title": "My YouTube Live Stream",
    "description": "Live stream powered by Streamlit",
    "privacy_status": "public",
    "stream_preset": "720p30",
    "enable_dvr": True,
    "enable_360": False,
    "enable_chat": True,
    "self_declared_made_for_kids": False
}