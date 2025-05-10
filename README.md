# Streamlit Chat App with Local AI

A Streamlit-based chat application that interfaces with local AI models through Ollama.

## Features

- Chat interface with local AI models
- Support for multiple models (llama2, mistral, codellama)
- Adjustable temperature and token settings
- Real-time logging
- Debug mode for development
- Docker support for easy deployment

## Prerequisites

- Python 3.11+
- Docker
- Ollama (for local AI models)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running with Docker

1. Build the Docker image:
```bash
docker build -t streamlit-chat-app .
```

2. Run the container:
```bash
docker run -p 8502:8502 streamlit-chat-app
```

The app will be available at `http://localhost:8502`

## Running Locally

1. Start Ollama service
2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Configuration

- Model selection: Choose between llama2, mistral, or codellama
- Temperature: Adjust the creativity of responses (0.0 to 1.0)
- Max Tokens: Control response length
- Debug Mode: Enable for detailed logging

## Network Access

To access the app from other machines in your network:
1. Find your local IP address
2. Access the app at `http://<your-ip>:8502`

## License

MIT License 