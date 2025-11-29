"""MCP Client implementation for communicating with MCP servers."""

import ast
import json
import operator


class MCPClient:
    """Client for interacting with MCP servers."""

    def __init__(self, server_url=None):
        """Initialize the MCP client.

        Args:
            server_url: URL of the MCP server (optional for local mode).
        """
        self.server_url = server_url
        self.connected = False
        self._capabilities = {}

    def connect(self):
        """Establish connection to the MCP server.

        Returns:
            Boolean indicating connection success.
        """
        # Simulate connection for demo purposes
        self.connected = True
        self._capabilities = {
            "tools": True,
            "prompts": True,
            "resources": True,
        }
        return self.connected

    def disconnect(self):
        """Disconnect from the MCP server."""
        self.connected = False
        self._capabilities = {}

    def call_tool(self, tool_name, params=None):
        """Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call.
            params: Dictionary of parameters for the tool.

        Returns:
            Result from the tool execution.
        """
        if params is None:
            params = {}

        # Simulate tool call response
        return {
            "success": True,
            "tool": tool_name,
            "result": self._simulate_tool_result(tool_name, params),
        }

    def _simulate_tool_result(self, tool_name, params):
        """Simulate tool execution results.

        Args:
            tool_name: Name of the tool.
            params: Tool parameters.

        Returns:
            Simulated result based on tool type.
        """
        calc_result = 0
        if params.get("expression"):
            calc_result = self._safe_eval(str(params.get("expression")))
        
        simulated_results = {
            "get_weather": {"temperature": 72, "condition": "sunny", "location": params.get("location", "Unknown")},
            "search": {"results": ["Result 1", "Result 2", "Result 3"], "query": params.get("query", "")},
            "calculator": {"result": calc_result},
        }
        return simulated_results.get(tool_name, {"message": f"Tool '{tool_name}' executed successfully"})

    def _safe_eval(self, expression):
        """Safely evaluate a mathematical expression.

        Args:
            expression: Mathematical expression string.

        Returns:
            Result of the calculation or 0 if invalid.
        """
        # Define allowed operators
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        def _eval(node):
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                return operators[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                return operators[type(node.op)](operand)
            else:
                raise ValueError(f"Unsupported operation: {type(node)}")

        try:
            tree = ast.parse(expression, mode='eval')
            return _eval(tree.body)
        except (ValueError, KeyError, SyntaxError, TypeError):
            return 0

    def list_tools(self):
        """Get list of available tools from the server.

        Returns:
            List of tool definitions.
        """
        return [
            {"name": "get_weather", "description": "Get weather information for a location"},
            {"name": "search", "description": "Search for information"},
            {"name": "calculator", "description": "Perform mathematical calculations"},
        ]

    def get_capabilities(self):
        """Get server capabilities.

        Returns:
            Dictionary of server capabilities.
        """
        return self._capabilities
