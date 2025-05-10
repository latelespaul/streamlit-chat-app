import streamlit as st
import requests
from datetime import datetime
import json
import logging
import os
from logging.handlers import RotatingFileHandler

# Set up logging
def setup_logger():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging
    logger = logging.getLogger('chat_app')
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    stream_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # File handler (rotating log file)
    file_handler = RotatingFileHandler(
        'logs/chat_app.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Stream handler for Streamlit
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(stream_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger

# Initialize logger
logger = setup_logger()

# Set up the Streamlit page with a custom theme
st.set_page_config(
    page_title="🤖 Local AI Chat",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .stButton>button {
        border-radius: 20px;
        width: 100%;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
    .chat-message .content {
        display: flex;
        flex-direction: column;
    }
    .error-message {
        color: #ff4b4b;
        padding: 10px;
        border-radius: 5px;
        background-color: #ffebee;
    }
    .log-container {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        font-family: monospace;
        font-size: 12px;
        max-height: 200px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Model endpoint configuration
    model_endpoint = st.text_input(
        "Model Endpoint",
        value="http://host.docker.internal:11434/api/generate",
        help="The endpoint where your local model is running"
    )
    
    model_name = st.selectbox(
        "Select Model",
        ["llama2", "mistral", "codellama"],
        index=0
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.number_input("Max Tokens", 100, 2000, 500, 100)
    
    # Debug mode toggle
    debug_mode = st.checkbox("Enable Debug Mode", value=False)
    
    # Log level selection
    log_level = st.selectbox(
        "Log Level",
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        index=1
    )
    
    # Update log level
    logger.setLevel(getattr(logging, log_level))
    
    st.markdown("---")
    st.markdown("### 📝 About")
    st.markdown("This is a chat interface for your local AI model.")
    st.markdown("Made with ❤️ using Streamlit")

# Main chat interface
st.title("🤖 Chat with Local AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    logger.info("Initialized new chat session")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    logger.info(f"User input received: {prompt[:50]}...")
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare the request payload
                payload = {
                    "model": model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                }
                
                logger.debug(f"Request payload: {json.dumps(payload)}")
                
                if debug_mode:
                    st.write("Request Payload:", json.dumps(payload, indent=2))
                
                # Make the request
                logger.info(f"Sending request to {model_endpoint}")
                response = requests.post(
                    model_endpoint,
                    json=payload,
                    timeout=30
                )
                
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                
                if debug_mode:
                    st.write("Response Status:", response.status_code)
                    st.write("Response Headers:", dict(response.headers))
                
                if response.status_code == 200:
                    try:
                        # Handle the response as a single JSON object
                        response_data = response.json()
                        bot_response = response_data.get("response", "No response from model")
                        
                        # Add bot response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                        
                        # Display bot response
                        st.markdown(bot_response)
                        
                    except json.JSONDecodeError as e:
                        error_msg = f"Error parsing response: {str(e)}"
                        logger.error(error_msg)
                        st.error(error_msg)
                else:
                    error_msg = f"Error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    st.error(error_msg)
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Error connecting to the model: {str(e)}"
                logger.error(error_msg)
                st.error(error_msg)

# Display recent logs in the sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📋 Recent Logs")
    
    # Read the last 10 lines of the log file
    try:
        with open('logs/chat_app.log', 'r') as f:
            logs = f.readlines()[-10:]
            log_text = ''.join(logs)
            st.markdown(f'<div class="log-container">{log_text}</div>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.info("No logs available yet")

# Add a clear chat button in the sidebar
if st.sidebar.button("Clear Chat"):
    logger.info("Clearing chat history")
    st.session_state.messages = []
    st.rerun()
