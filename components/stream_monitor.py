import streamlit as st
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_utils import get_stream_health, get_stream_analytics

def render_stream_monitor():
    """Render the stream monitor tab content"""
    
    st.header("Live Stream Monitor")
    
    # Check if stream is active
    if not st.session_state.streaming:
        st.warning("⚠️ Stream is not active. Start streaming to see live metrics.")
    
    # Stream Health and Stats section
    col1, col2, col3 = st.columns(3)
    
    stream_health = get_stream_health()
    analytics = get_stream_analytics()
    
    with col1:
        render_health_card(stream_health)
    
    with col2:
        st.markdown("### Viewers")
        if st.session_state.streaming:
            with st.container(border=True):
                value = stream_health.get("viewers", 0)
                st.markdown(f"<h1 style='text-align: center; font-size: 3rem;'>{value}</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center;'>Current Viewers</p>", unsafe_allow_html=True)
        else:
            with st.container(border=True):
                st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #9e9e9e;'>0</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center;'>Current Viewers</p>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("### Likes")
        if st.session_state.streaming and analytics.get("likes"):
            with st.container(border=True):
                value = analytics.get("total_likes", 0)
                st.markdown(f"<h1 style='text-align: center; font-size: 3rem;'>{value}</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center;'>Total Likes</p>", unsafe_allow_html=True)
        else:
            with st.container(border=True):
                st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #9e9e9e;'>0</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center;'>Total Likes</p>", unsafe_allow_html=True)
    
    # Viewer graph
    st.markdown("### Viewer Trend")
    
    if analytics.get("times") and analytics.get("viewers"):
        # Create a Plotly line chart for viewers
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=analytics["times"],
            y=analytics["viewers"],
            mode='lines+markers',
            name='Viewers',
            line=dict(color='#FF0000', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 0, 0, 0.1)'
        ))
        
        # Layout configuration
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="Time",
            yaxis_title="Viewers",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Start streaming to see viewer trends")
        
        # Create a placeholder chart
        fig = go.Figure()
        
        # Create some sample data
        x = [f"{i:02d}:00" for i in range(24)]
        y = [0 for _ in range(24)]
        
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color='#e0e0e0', width=2),
            fill='tozeroy',
            fillcolor='rgba(224, 224, 224, 0.1)'
        ))
        
        # Layout configuration
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="Time",
            yaxis_title="Viewers",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Technical Info Section
    st.markdown("### Technical Stream Info")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            if st.session_state.streaming:
                # Get the stream settings
                settings = st.session_state.stream_settings
                preset = settings["stream_preset"]
                
                st.markdown("#### Stream Configuration")
                st.markdown(f"**Title:** {settings['title']}")
                st.markdown(f"**Privacy:** {settings['privacy']} status")
                st.markdown(f"**Quality:** {preset}")
                st.markdown(f"**Chat Enabled:** {'Yes' if settings['enable_chat'] else 'No'}")
            else:
                st.markdown("#### Stream Configuration")
                st.markdown("*Stream not active*")
    
    with col2:
        with st.container(border=True):
            if st.session_state.streaming:
                # In a real app, this would show actual server info
                st.markdown("#### Server Information")
                st.markdown("**Region:** US East")
                st.markdown("**Server:** rtmp-live-useast1-002.youtube.com")
                st.markdown("**Connection:** Established")
                st.markdown("**Uptime:** " + get_uptime_string())
            else:
                st.markdown("#### Server Information")
                st.markdown("*Stream not active*")
    
    # Auto-refresh section
    st.markdown("### Auto-refresh")
    auto_refresh = st.checkbox("Enable auto-refresh (10 seconds)", value=True)
    
    if auto_refresh and st.session_state.streaming:
        # Add a progress bar that resets every 10 seconds
        progress_bar = st.progress(0)
        
        # This would normally be implemented with JavaScript, but in Streamlit we can't do that
        # In a real app, we'd use a periodic callback or JavaScript for this
        for i in range(10):
            # Update progress bar
            progress_bar.progress((i+1)/10)
            time.sleep(1)
            
        # Uncomment below in a real app to trigger page refresh
        # st.experimental_rerun()
    
    # End streaming button
    if st.session_state.streaming:
        st.markdown("### Stream Control")
        if st.button("End Stream", type="primary", use_container_width=True):
            with st.spinner("Stopping stream..."):
                time.sleep(1)  # Simulate shutdown delay
                st.session_state.streaming = False
                st.success("Stream ended successfully")
                st.experimental_rerun()

def render_health_card(health_data):
    """Render a health status card"""
    
    st.markdown("### Stream Health")
    
    if not st.session_state.streaming:
        with st.container(border=True):
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown("<h2 style='color: #9e9e9e;'>Offline</h2>", unsafe_allow_html=True)
            st.markdown("<div style='background-color: #e0e0e0; height: 8px; border-radius: 4px;'></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Determine color based on health status
    health_value = health_data.get("health", 0)
    if health_value > 90:
        color = "#4CAF50"  # Green
        status = "Excellent"
    elif health_value > 75:
        color = "#8BC34A"  # Light Green
        status = "Good"
    elif health_value > 50:
        color = "#FFC107"  # Amber
        status = "Fair"
    else:
        color = "#F44336"  # Red
        status = "Poor"
    
    with st.container(border=True):
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: {color};'>{status}</h2>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='background-color: #e0e0e0; height: 8px; border-radius: 4px;'>
                <div style='width: {health_value}%; background-color: {color}; height: 100%; border-radius: 4px;'></div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

def get_uptime_string():
    """Get a formatted uptime string"""
    
    if not st.session_state.streaming or not st.session_state.stream_start_time:
        return "00:00:00"
    
    duration = datetime.now() - st.session_state.stream_start_time
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"