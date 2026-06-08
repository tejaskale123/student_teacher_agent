from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class FormatterAgent:

    def __init__(self):

        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def format(self, answer):

        prompt = f"""
You are an expert AI teacher and content formatter.

Your job is to convert raw AI answers into
professional, easy-to-read responses.

Rules:

1. Always create a title.

2. Add:
   - Summary
   - Main Explanation
   - Key Points
   - Example (if applicable)
   - Conclusion

3. Use bullet points.

4. Preserve URLs exactly.

5. If answer contains search results:

Format:

# Search Results

## Top Sources

1. Title
   URL

2. Title
   URL

## Key Insights

...

## Recommendation

...

6. If answer contains comparison:

Format:

# Comparison Report

## PDF Findings

...

## Search Findings

...

## Similarities

...

## Differences

...

## Conclusion

7. If answer contains calculations:

Format:

# Calculation Result

Expression:
...

Answer:
...

8. Make answer look like ChatGPT.

Raw Answer:

{answer}
"""

        return self.llm.ask(prompt)