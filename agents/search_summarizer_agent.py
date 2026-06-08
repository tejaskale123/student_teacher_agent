from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class SearchSummarizerAgent:

    def __init__(self):
        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def summarize(self, search_result):

        prompt = f"""
You are a careful search-result summarization expert.

Convert the raw search results into:

# Topic

## Top Updates

- Important update 1
- Important update 2
- Important update 3

## Key Insights

- Insight 1
- Insight 2

## Sources

Keep all useful URLs.

Strict rules:

- Use ONLY the titles, snippets, and URLs present in Search Results.
- NEVER invent release numbers, dates, facts, features, or company announcements.
- If a result only looks like a general news/resource page, describe it as a source/resource, not as a specific update.
- If the search results do not contain enough detail for a concrete update, say that the source may contain updates instead of guessing.
- Preserve all useful URLs exactly.
- Do not use outside knowledge.
- Do not describe websites.
- Bad: "Python.org provides blogs"
- Bad: "Real Python provides tutorials"
- Good: "The search results point to community updates, tutorials, and Python ecosystem news."
- Good: "The available sources suggest ongoing Python development and learning resources."

Search Results:

{search_result}
"""

        return self.llm.ask(prompt)
