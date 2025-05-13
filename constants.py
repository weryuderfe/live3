# YouTube RTMP streaming configuration
RTMP_URL = "rtmp://a.rtmp.youtube.com/live2"

# Default stream settings
DEFAULT_STREAM_SETTINGS = {
    "stream_preset": "720p30",
    "resolution": "1280x720",
    "fps": 30,
    "bitrate": "3000k",
    "audio_bitrate": "128k"
}

# Supported video formats
SUPPORTED_VIDEO_FORMATS = ["mp4", "webm", "mov"]

# Maximum video file size (100MB)
MAX_VIDEO_SIZE = 100 * 1024 * 1024
