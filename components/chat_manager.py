import streamlit as st
import random
import time
from datetime import datetime
from streamlit_utils import get_live_chat_messages, send_chat_message
from constants import CHAT_MESSAGE_TYPES, MODERATION_ACTIONS

def render_chat_manager():
    """Render the live chat manager tab content"""
    
    st.header("Live Chat Manager")
    
    # Check if stream is active
    if not st.session_state.streaming:
        st.warning("⚠️ Stream is not active. Start streaming to manage chat.")
    
    # Check if chat is enabled in settings
    if "stream_settings" in st.session_state and not st.session_state.stream_settings.get("enable_chat", True):
        st.error("❌ Live chat is disabled in your stream settings.")
        
        if st.button("Enable Chat", use_container_width=True):
            st.session_state.stream_settings["enable_chat"] = True
            st.success("Chat enabled for this stream.")
            st.experimental_rerun()
            
        return
    
    # Initialize chat history if not present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Moderation Settings
    with st.expander("Chat Moderation Settings", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Auto-block spam", value=True, help="Automatically block potential spam messages")
            st.checkbox("Slow mode", value=False, help="Limit how often viewers can send messages")
            st.checkbox("Subscriber-only mode", value=False, help="Only channel subscribers can chat")
            
        with col2:
            st.number_input("Slow mode delay (seconds)", min_value=1, max_value=120, value=30, step=1)
            st.selectbox("Blocked words filter", options=["Off", "Low", "Medium", "High"], index=1)
            st.checkbox("Hold potentially inappropriate messages for review", value=True)
    
    # Chat display and interaction
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Live Chat")
        
        # Get the latest chat messages
        if st.session_state.streaming:
            new_messages = get_live_chat_messages()
            # Add new messages to history
            for msg in new_messages:
                if msg not in st.session_state.chat_history:
                    st.session_state.chat_history.append(msg)
        
        # Display chat container
        with st.container(height=400, border=True):
            # Get the latest 50 messages to display
            messages_to_display = st.session_state.chat_history[-50:] if st.session_state.chat_history else []
            
            if not messages_to_display:
                if st.session_state.streaming:
                    st.info("Waiting for chat messages...")
                else:
                    st.info("Chat messages will appear here when streaming is active.")
            
            # Display messages from oldest to newest
            for msg in messages_to_display:
                render_chat_message(msg)
        
        # Message input
        if st.session_state.streaming:
            with st.form("chat_form", clear_on_submit=True):
                chat_input = st.text_input("Type your message", key="chat_input", max_chars=200)
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    submit = st.form_submit_button("Send", use_container_width=True)
                
                with col2:
                    st.markdown("""
                        <style>
                            .streaming-tag {
                                display: inline-block;
                                padding: 2px 8px;
                                background-color: #FF0000;
                                color: white;
                                border-radius: 10px;
                                font-size: 0.8em;
                                animation: pulse 2s infinite;
                            }
                            
                            @keyframes pulse {
                                0% { opacity: 1; }
                                50% { opacity: 0.7; }
                                100% { opacity: 1; }
                            }
                        </style>
                        <div style="display: flex; align-items: center;">
                            <div class="streaming-tag">LIVE</div>
                            <span style="margin-left: 8px;">Posting as Channel Owner</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                if submit and chat_input:
                    with st.spinner("Sending message..."):
                        success = send_chat_message(chat_input)
                        
                        if success:
                            # Add the message to our history
                            new_msg = {
                                "id": f"owner_msg_{int(time.time())}",
                                "author": "You (Channel Owner)",
                                "message": chat_input,
                                "timestamp": datetime.now().strftime("%H:%M:%S"),
                                "type": "owner_message"
                            }
                            st.session_state.chat_history.append(new_msg)
                            st.experimental_rerun()
                        else:
                            st.error("Failed to send message. Please try again.")
        else:
            st.info("Start streaming to send chat messages.")
    
    with col2:
        st.markdown("### Quick Actions")
        
        # Quick message buttons
        st.markdown("#### Quick Responses")
        
        quick_messages = [
            "Thanks for watching!",
            "Welcome to the stream!",
            "Don't forget to like!",
            "Thanks for the support!",
            "I'll answer that soon!"
        ]
        
        for msg in quick_messages:
            if st.button(msg, key=f"quick_{msg}", use_container_width=True):
                if st.session_state.streaming:
                    with st.spinner("Sending message..."):
                        success = send_chat_message(msg)
                        
                        if success:
                            # Add the message to our history
                            new_msg = {
                                "id": f"quick_msg_{int(time.time())}",
                                "author": "You (Channel Owner)",
                                "message": msg,
                                "timestamp": datetime.now().strftime("%H:%M:%S"),
                                "type": "owner_message"
                            }
                            st.session_state.chat_history.append(new_msg)
                            st.experimental_rerun()
                else:
                    st.warning("Start streaming to send messages.")
        
        # Moderation actions
        st.markdown("#### Moderation")
        
        # Show available moderation actions
        moderation_action = st.selectbox(
            "Select Action", 
            options=list(MODERATION_ACTIONS.keys()),
            format_func=lambda x: MODERATION_ACTIONS[x]
        )
        
        if st.button("Apply to Selected", type="primary", use_container_width=True):
            st.warning("No user selected. Select a user's message first.")
        
        # Refresh button
        if st.button("Refresh Chat", use_container_width=True):
            with st.spinner("Refreshing..."):
                time.sleep(0.5)  # Simulate refresh
                st.experimental_rerun()

def render_chat_message(message):
    """Render a single chat message with appropriate styling"""
    
    author = message.get("author", "Anonymous")
    msg_text = message.get("message", "")
    timestamp = message.get("timestamp", "00:00:00")
    msg_type = message.get("type", "regular")
    
    # Determine styling based on message type
    if msg_type == "owner_message":
        background_color = "#e1f5fe"
        author_color = "#01579b"
        icon = "👑"
    elif msg_type == "super_chat":
        background_color = "#ffebee"
        author_color = "#FF0000"
        icon = "💰"
    elif msg_type == "membership":
        background_color = "#e8f5e9"
        author_color = "#388e3c"
        icon = "🎉"
    else:
        background_color = "#f5f5f5"
        author_color = "#424242"
        icon = ""
    
    # Render the message
    st.markdown(
        f"""
        <div style="background-color: {background_color}; padding: 8px 12px; border-radius: 8px; margin-bottom: 8px;">
            <div>
                <span style="font-weight: bold; color: {author_color};">{icon} {author}</span>
                <span style="font-size: 0.8em; color: #9e9e9e; margin-left: 8px;">{timestamp}</span>
            </div>
            <div style="margin-top: 4px;">{msg_text}</div>
            {f'<div style="margin-top: 4px; font-weight: bold; color: #D50000;">{message.get("amount")}</div>' if msg_type == "super_chat" and message.get("amount") else ''}
        </div>
        """,
        unsafe_allow_html=True
    )