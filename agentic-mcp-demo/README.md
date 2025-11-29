# Agentic MCP Demo

A demonstration of the Model Context Protocol (MCP) integration with an agentic LLM simulator.

## Overview

This project demonstrates how MCP (Model Context Protocol) can be used to extend LLM capabilities by providing external tools and data sources. It includes:

- **Backend**: A Python-based server with LLM simulation and MCP client/server implementation
- **Frontend**: A simple web interface to interact with the system

## Project Structure

```
agentic-mcp-demo/
├── README.md
├── requirements.txt
├── backend/
│   ├── main.py              # Main application entry point
│   ├── llm_simulator.py     # LLM simulation logic
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── client.py        # MCP client implementation
│   │   └── server.py        # MCP server implementation
│   └── data/
│       ├── llmResponses.json       # Predefined LLM responses
│       └── mcpServerResponses.json # MCP server response templates
└── frontend/
    ├── index.html           # Main HTML page
    ├── script.js            # Frontend JavaScript
    └── styles.css           # Styling
```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the backend server:
   ```bash
   cd backend
   python main.py
   ```

2. Open `frontend/index.html` in your browser or serve it with a local server.

## Features

- LLM response simulation
- MCP protocol client/server communication
- Web-based interface for interaction
- Extensible architecture for adding new tools

## License

MIT License
