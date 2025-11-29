"""Main application entry point for the Agentic MCP Demo."""

import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from llm_simulator import LLMSimulator
from mcp.client import MCPClient
from mcp.server import MCPServer

app = Flask(__name__)
CORS(app)

# Initialize components
llm_simulator = LLMSimulator()
mcp_server = MCPServer()
mcp_client = MCPClient()


@app.route("/", methods=["GET"])
def index():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Agentic MCP Demo Backend"})


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat requests and simulate LLM responses."""
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Get LLM response
    response = llm_simulator.generate_response(user_message)

    # Check if MCP tool call is needed
    if response.get("requires_tool"):
        tool_result = mcp_client.call_tool(
            response.get("tool_name"), response.get("tool_params", {})
        )
        response["tool_result"] = tool_result

    return jsonify(response)


@app.route("/api/tools", methods=["GET"])
def list_tools():
    """List available MCP tools."""
    tools = mcp_server.list_tools()
    return jsonify({"tools": tools})


@app.route("/api/tools/<tool_name>", methods=["POST"])
def execute_tool(tool_name):
    """Execute a specific MCP tool."""
    data = request.get_json() or {}
    result = mcp_server.execute_tool(tool_name, data)
    return jsonify(result)


def main():
    """Run the Flask application."""
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
