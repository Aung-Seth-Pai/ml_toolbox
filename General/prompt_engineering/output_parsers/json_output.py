import json
import re
from langchain_core.output_parsers import BaseOutputParser

class JsonOutputParser(BaseOutputParser[dict]):
    """
    Parses a JSON string output from the model into a Python dict.
    Automatically removes any stray text or <think> blocks before parsing.
    """

    def parse(self, text: str) -> dict:
        # Remove <think>...</think> blocks (if any)
        cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)

        # Strip whitespace
        cleaned = cleaned.strip()

        # Ensure only JSON is extracted (in case model adds backticks)
        # Remove leading/trailing backticks or quotes
        cleaned = cleaned.strip("`\"'")

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from model output: {cleaned}") from e
