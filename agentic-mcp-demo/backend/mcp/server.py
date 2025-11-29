"""MCP Server implementation for handling tool requests."""

import ast
import json
import operator
import os


class MCPServer:
    """Server for handling MCP tool requests."""

    def __init__(self, responses_file=None):
        """Initialize the MCP server.

        Args:
            responses_file: Path to JSON file with server responses.
        """
        if responses_file is None:
            responses_file = os.path.join(
                os.path.dirname(__file__), "..", "data", "mcpServerResponses.json"
            )
        self.responses = self._load_responses(responses_file)
        self._tools = self._initialize_tools()

    def _load_responses(self, filepath):
        """Load responses from JSON file.

        Args:
            filepath: Path to the JSON file.

        Returns:
            Dictionary of server responses.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _initialize_tools(self):
        """Initialize available tools.

        Returns:
            Dictionary of tool definitions.
        """
        return {
            "get_weather": {
                "name": "get_weather",
                "description": "Get current weather for a specified location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city or location to get weather for",
                        }
                    },
                    "required": ["location"],
                },
            },
            "search": {
                "name": "search",
                "description": "Search for information on a given topic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query",
                        }
                    },
                    "required": ["query"],
                },
            },
            "calculator": {
                "name": "calculator",
                "description": "Perform mathematical calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }

    def list_tools(self):
        """Get list of all available tools.

        Returns:
            List of tool definitions.
        """
        return list(self._tools.values())

    def get_tool(self, tool_name):
        """Get a specific tool by name.

        Args:
            tool_name: Name of the tool.

        Returns:
            Tool definition or None if not found.
        """
        return self._tools.get(tool_name)

    def execute_tool(self, tool_name, params=None):
        """Execute a tool with given parameters.

        Args:
            tool_name: Name of the tool to execute.
            params: Dictionary of parameters.

        Returns:
            Execution result.
        """
        if params is None:
            params = {}

        if tool_name not in self._tools:
            return {"error": f"Tool '{tool_name}' not found", "success": False}

        # Check for predefined responses
        tool_responses = self.responses.get("tools", {}).get(tool_name, {})

        # Execute tool based on type
        handlers = {
            "get_weather": self._handle_weather,
            "search": self._handle_search,
            "calculator": self._handle_calculator,
        }

        handler = handlers.get(tool_name, self._handle_default)
        return handler(params, tool_responses)

    def _handle_weather(self, params, responses):
        """Handle weather tool execution.

        Args:
            params: Tool parameters.
            responses: Predefined responses.

        Returns:
            Weather data result.
        """
        location = params.get("location", "Unknown")
        default_response = responses.get("default", {})
        return {
            "success": True,
            "data": {
                "location": location,
                "temperature": default_response.get("temperature", 72),
                "condition": default_response.get("condition", "sunny"),
                "humidity": default_response.get("humidity", 45),
            },
        }

    def _handle_search(self, params, responses):
        """Handle search tool execution.

        Args:
            params: Tool parameters.
            responses: Predefined responses.

        Returns:
            Search results.
        """
        query = params.get("query", "")
        default_results = responses.get("default", {}).get(
            "results", ["No results found"]
        )
        return {
            "success": True,
            "data": {
                "query": query,
                "results": default_results,
                "total": len(default_results),
            },
        }

    def _handle_calculator(self, params, responses):
        """Handle calculator tool execution.

        Args:
            params: Tool parameters.
            responses: Predefined responses.

        Returns:
            Calculation result.
        """
        expression = params.get("expression", "0")
        try:
            result = self._safe_eval(str(expression))
            return {"success": True, "data": {"expression": expression, "result": result}}
        except (SyntaxError, TypeError, ValueError) as e:
            return {"success": False, "error": f"Calculation error: {e!s}"}

    def _safe_eval(self, expression):
        """Safely evaluate a mathematical expression using AST.

        Args:
            expression: Mathematical expression string.

        Returns:
            Result of the calculation.

        Raises:
            ValueError: If the expression contains unsupported operations.
        """
        # Define allowed operators
        operators_map = {
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
                return operators_map[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                return operators_map[type(node.op)](operand)
            else:
                raise ValueError(f"Unsupported operation: {type(node)}")

        tree = ast.parse(expression, mode='eval')
        return _eval(tree.body)

    def _handle_default(self, params, responses):
        """Handle default tool execution.

        Args:
            params: Tool parameters.
            responses: Predefined responses.

        Returns:
            Default response.
        """
        return {
            "success": True,
            "data": {"message": "Tool executed", "params": params},
        }
