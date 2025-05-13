# YouTube RTMP Streaming Tool

A beautiful, professional streaming dashboard built with Python and Streamlit to manage YouTube live streams via RTMP.

## Features

- **Stream Key Management**: Securely store and use your YouTube stream key
- **Live Stream Monitoring**: Real-time analytics and health monitoring
- **Chat Integration**: View and respond to live chat messages
- **Stream Analytics**: Comprehensive performance metrics and audience insights
- **Stream Configuration**: Easily configure stream settings and encoder parameters

## Getting Started

### Prerequisites

- Python 3.8 or higher
- YouTube account with live streaming enabled
- Stream key from YouTube Studio

### Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

## Usage

1. Start the application
2. Authenticate with your YouTube account
3. Enter your stream key in the Setup tab
4. Configure your stream settings
5. Use the Start Stream button to begin broadcasting
6. Monitor your stream stats and chat in real-time
7. Analyze your performance after the stream

## RTMP URL

This tool is preconfigured to use YouTube's RTMP ingest server:

```
rtmp://a.rtmp.youtube.com/live2
```

## Tech Stack

- **Streamlit**: Frontend UI framework
- **Plotly**: Interactive charts and visualizations
- **YouTube API**: For integration with YouTube streaming services
- **FFmpeg**: For handling streaming media (via ffmpeg-python)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This project is not affiliated with, authorized by, endorsed by, or in any way officially connected with YouTube or Google LLC. The official YouTube website can be found at youtube.com.