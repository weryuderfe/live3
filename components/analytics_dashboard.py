import streamlit as st
import plotly.graph_objects as go
from streamlit_utils import get_stream_analytics

def render_analytics_dashboard():
    """Render the analytics dashboard tab content"""
    
    st.header("Stream Analytics")
    
    # Tabs for different analysis views
    tab1, tab2, tab3 = st.tabs(["Overview", "Audience", "Performance"])
    
    # Get analytics data
    analytics = get_stream_analytics()
    
    with tab1:
        render_overview_tab(analytics)
    
    with tab2:
        render_audience_tab(analytics)
    
    with tab3:
        render_performance_tab(analytics)

def render_overview_tab(analytics):
    """Render the overview analytics tab"""
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card("Peak Viewers", analytics.get("peak_viewers", 0))
    
    with col2:
        render_metric_card("Avg. Viewers", analytics.get("avg_viewers", 0))
    
    with col3:
        render_metric_card("Total Likes", analytics.get("total_likes", 0))
    
    with col4:
        render_metric_card("Comments", analytics.get("comments", 0))
    
    # Viewer and engagement graph
    st.markdown("### Viewer Trends")
    
    if analytics.get("times") and analytics.get("viewers") and analytics.get("likes"):
        # Create a Plotly line chart for viewers and likes
        fig = go.Figure()
        
        # Add viewers line
        fig.add_trace(go.Scatter(
            x=analytics["times"],
            y=analytics["viewers"],
            mode='lines+markers',
            name='Viewers',
            line=dict(color='#FF0000', width=3),
        ))
        
        # Add likes line
        fig.add_trace(go.Scatter(
            x=analytics["times"],
            y=analytics["likes"],
            mode='lines+markers',
            name='Likes',
            line=dict(color='#4CAF50', width=3),
        ))
        
        # Layout configuration
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="Time",
            yaxis_title="Count",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
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
        st.info("Start streaming to see analytics data")
    
    # Key moments
    st.markdown("### Key Moments")
    
    if st.session_state.streaming or len(analytics.get("viewers", [])) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container(border=True):
                st.markdown("#### Peak Viewership")
                
                if len(analytics.get("viewers", [])) > 0:
                    max_index = analytics["viewers"].index(max(analytics["viewers"]))
                    max_time = analytics["times"][max_index]
                    
                    st.markdown(f"**Time:** {max_time}")
                    st.markdown(f"**Viewers:** {max(analytics['viewers'])}")
                    st.markdown("**Possible Cause:** High engagement content or external promotion")
                else:
                    st.info("No peak data available yet")
        
        with col2:
            with st.container(border=True):
                st.markdown("#### Engagement Spike")
                
                if len(analytics.get("likes", [])) > 0:
                    # Find where likes increased the most between intervals
                    like_diffs = [analytics["likes"][i] - analytics["likes"][i-1] for i in range(1, len(analytics["likes"]))]
                    
                    if like_diffs:
                        max_diff_index = like_diffs.index(max(like_diffs)) + 1
                        spike_time = analytics["times"][max_diff_index]
                        
                        st.markdown(f"**Time:** {spike_time}")
                        st.markdown(f"**Likes Added:** +{like_diffs[max_diff_index-1]}")
                        st.markdown("**Possible Cause:** Engaging content or call to action")
                    else:
                        st.info("No engagement spike data available yet")
                else:
                    st.info("No engagement data available yet")
        
        # Recommendations based on analytics
        st.markdown("### Recommendations")
        
        with st.container(border=True):
            st.markdown("""
                - **Optimal Stream Length:** 45-60 minutes based on viewer retention
                - **Best Stream Time:** Weekdays between 6-8 PM for your audience
                - **Content Type:** Tutorial and discussion content has higher engagement
                - **Engagement Tip:** Ask questions to your audience every 10-15 minutes
            """)
    else:
        st.info("Start streaming to see key moments and recommendations")

def render_audience_tab(analytics):
    """Render the audience analytics tab"""
    
    st.markdown("### Audience Breakdown")
    
    # In a real app, this would show actual audience demographics
    # This is just a mockup with sample data
    
    # Device breakdown
    st.markdown("#### Viewing Devices")
    
    # Sample device data
    devices = {
        "Mobile": 45,
        "Desktop": 35,
        "TV": 15,
        "Tablet": 5
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(devices.keys()),
        values=list(devices.values()),
        hole=.4,
        marker_colors=['#FF0000', '#4285F4', '#34A853', '#FBBC05']
    )])
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Traffic sources
    st.markdown("#### Traffic Sources")
    
    # Sample traffic source data
    sources = {
        "Subscriptions": 30,
        "Browse features": 25,
        "YouTube search": 20,
        "External": 15,
        "Notifications": 10
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create a horizontal bar chart
        fig = go.Figure(go.Bar(
            x=list(sources.values()),
            y=list(sources.keys()),
            orientation='h',
            marker_color=['#FF0000', '#4285F4', '#34A853', '#FBBC05', '#EA4335']
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="Percentage",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Top External Sources")
        
        # Sample external sources
        external_sources = [
            {"source": "Google Search", "percentage": "45%"},
            {"source": "Twitter", "percentage": "25%"},
            {"source": "Facebook", "percentage": "15%"},
            {"source": "Reddit", "percentage": "10%"},
            {"source": "Other", "percentage": "5%"}
        ]
        
        for source in external_sources:
            st.markdown(f"**{source['source']}**: {source['percentage']}")
    
    # Geographic distribution
    st.markdown("#### Geographic Distribution")
    
    # Sample location data
    locations = {
        "United States": 40,
        "United Kingdom": 15,
        "Canada": 10,
        "Australia": 8,
        "Germany": 7,
        "India": 5,
        "Other": 15
    }
    
    fig = go.Figure(data=[go.Bar(
        x=list(locations.keys()),
        y=list(locations.values()),
        marker_color='#FF0000'
    )])
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="Country",
        yaxis_title="Percentage",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_performance_tab(analytics):
    """Render the performance analytics tab"""
    
    st.markdown("### Stream Performance")
    
    # Stream health over time
    st.markdown("#### Stream Health Metrics")
    
    # Sample health metrics over time
    times = analytics.get("times", [])
    if not times:
        st.info("Start streaming to see performance metrics")
        return
    
    # Generate some mock health metrics
    health_metrics = {
        "Resolution": [1080 if random.random() > 0.1 else 720 for _ in range(len(times))],
        "FPS": [60 if random.random() > 0.05 else int(60 * random.random() * 0.9) for _ in range(len(times))],
        "Bitrate (Mbps)": [5 + random.random() * 2 for _ in range(len(times))],
        "Buffer Health (%)": [95 + random.random() * 5 for _ in range(len(times))]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Resolution and FPS
        fig = go.Figure()
        
        # Add Resolution line
        fig.add_trace(go.Scatter(
            x=times,
            y=health_metrics["Resolution"],
            mode='lines',
            name='Resolution',
            line=dict(color='#4285F4', width=3),
        ))
        
        # Add second y-axis for FPS
        fig.add_trace(go.Scatter(
            x=times,
            y=health_metrics["FPS"],
            mode='lines',
            name='FPS',
            line=dict(color='#34A853', width=3),
            yaxis='y2'
        ))
        
        # Layout with dual y-axes
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="Time",
            yaxis_title="Resolution (p)",
            yaxis2=dict(
                title="FPS",
                overlaying='y',
                side='right'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
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
    
    with col2:
        # Bitrate and Buffer Health
        fig = go.Figure()
        
        # Add Bitrate line
        fig.add_trace(go.Scatter(
            x=times,
            y=health_metrics["Bitrate (Mbps)"],
            mode='lines',
            name='Bitrate',
            line=dict(color='#FBBC05', width=3),
        ))
        
        # Add second y-axis for Buffer Health
        fig.add_trace(go.Scatter(
            x=times,
            y=health_metrics["Buffer Health (%)"],
            mode='lines',
            name='Buffer Health',
            line=dict(color='#EA4335', width=3),
            yaxis='y2'
        ))
        
        # Layout with dual y-axes
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="Time",
            yaxis_title="Bitrate (Mbps)",
            yaxis2=dict(
                title="Buffer Health (%)",
                overlaying='y',
                side='right'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
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
    
    # Playback performance
    st.markdown("#### Playback Performance")
    
    # Sample playback metrics
    playback_metrics = {
        "Average Watch Time": "8:45",
        "Play Rate": "92%",
        "Buffering Ratio": "1.2%",
        "Average Resolution": "1080p"
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card("Avg. Watch Time", playback_metrics["Average Watch Time"])
    
    with col2:
        render_metric_card("Play Rate", playback_metrics["Play Rate"])
    
    with col3:
        render_metric_card("Buffering Ratio", playback_metrics["Buffering Ratio"])
    
    with col4:
        render_metric_card("Avg. Resolution", playback_metrics["Average Resolution"])
    
    # Stream stability score
    st.markdown("#### Stream Stability Score")
    
    stability_score = 92  # Sample score out of 100
    
    # Determine color based on score
    if stability_score > 90:
        color = "#4CAF50"  # Green
        status = "Excellent"
    elif stability_score > 75:
        color = "#8BC34A"  # Light Green
        status = "Good"
    elif stability_score > 60:
        color = "#FFC107"  # Amber
        status = "Fair"
    else:
        color = "#F44336"  # Red
        status = "Poor"
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = stability_score,
            title = {'text': "Stability Score"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 60], 'color': "rgba(244, 67, 54, 0.2)"},
                    {'range': [60, 75], 'color': "rgba(255, 193, 7, 0.2)"},
                    {'range': [75, 90], 'color': "rgba(139, 195, 74, 0.2)"},
                    {'range': [90, 100], 'color': "rgba(76, 175, 80, 0.2)"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': stability_score
                }
            }
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(l=30, r=30, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"### {status} Stream Quality")
        
        if stability_score > 75:
            st.success("""
                Your stream is performing well with minimal issues. Viewers are experiencing high-quality playback with very little buffering.
                
                **Strengths:**
                - Consistent resolution and bitrate
                - Low buffering ratio
                - High play rate
            """)
        elif stability_score > 60:
            st.warning("""
                Your stream is performing adequately but experiencing some issues. Some viewers may experience occasional buffering or quality changes.
                
                **Areas for improvement:**
                - Stabilize your internet connection
                - Consider reducing your resolution or bitrate
                - Check for background processes using bandwidth
            """)
        else:
            st.error("""
                Your stream is experiencing significant issues. Many viewers may be experiencing frequent buffering or low quality.
                
                **Critical improvements needed:**
                - Check your internet connection and speed
                - Reduce resolution and bitrate immediately
                - Close all unnecessary applications
                - Consider using a wired connection
            """)

def render_metric_card(title, value):
    """Render a metric card for analytics"""
    
    with st.container(border=True):
        st.markdown(f"<p style='font-size: 0.9rem; color: #606060; margin-bottom: 5px;'>{title}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 1.5rem; font-weight: bold; margin: 0;'>{value}</p>", unsafe_allow_html=True)