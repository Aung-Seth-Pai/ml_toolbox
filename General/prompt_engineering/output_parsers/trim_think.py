import re
from langchain_core.output_parsers import BaseOutputParser

class TrimThinkOutputParser(BaseOutputParser[str]):
    def parse(self, text: str) -> str:
        '''
         to remove any content enclosed within <think>...</think> tags from the model's output.
        '''
        cleaned = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE # Ignore case to match <think> and </think> in any case
        )
        return cleaned.strip()
