"""LLM Simulator module for generating mock LLM responses."""

import json
import os
import re


class LLMSimulator:
    """Simulates LLM behavior with predefined responses."""

    def __init__(self, responses_file=None):
        """Initialize the LLM simulator.

        Args:
            responses_file: Path to JSON file with predefined responses.
        """
        if responses_file is None:
            responses_file = os.path.join(
                os.path.dirname(__file__), "data", "llmResponses.json"
            )
        self.responses = self._load_responses(responses_file)

    def _load_responses(self, filepath):
        """Load responses from JSON file.

        Args:
            filepath: Path to the JSON file.

        Returns:
            Dictionary of predefined responses.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"default": {"response": "I'm here to help!", "requires_tool": False}}

    def generate_response(self, user_input):
        """Generate a response based on user input.

        Args:
            user_input: The user's message.

        Returns:
            A dictionary containing the response and metadata.
        """
        user_input_lower = user_input.lower()

        # Check for matching patterns in predefined responses
        for pattern, response_data in self.responses.get("patterns", {}).items():
            if re.search(pattern, user_input_lower):
                return {
                    "message": response_data.get("response", ""),
                    "requires_tool": response_data.get("requires_tool", False),
                    "tool_name": response_data.get("tool_name"),
                    "tool_params": response_data.get("tool_params", {}),
                }

        # Return default response if no pattern matches
        default = self.responses.get("default", {})
        return {
            "message": default.get(
                "response", "I understand. How can I assist you further?"
            ),
            "requires_tool": default.get("requires_tool", False),
        }

    def get_available_patterns(self):
        """Get list of available response patterns.

        Returns:
            List of pattern strings.
        """
        return list(self.responses.get("patterns", {}).keys())
