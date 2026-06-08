from tavily import TavilyClient
from config import TAVILY_API_KEY


class SearchTool:

    def __init__(self):
        self.client = None

        if TAVILY_API_KEY:
            self.client = TavilyClient(
                api_key=TAVILY_API_KEY
            )

    def search(self, query):
        try:
            if not TAVILY_API_KEY:
                return "Search Error: TAVILY_API_KEY is missing in .env"

            print("Searching:", query)

            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=3
            )

            answer = ""

            for i, result in enumerate(
                response.get("results", []),
                start=1
            ):

                answer += (
                    f"{i}. "
                    f"{result.get('title', 'No Title')}\n"
                    f"{result.get('url', 'No URL')}\n"
                    f"{result.get('content', 'No content')}\n\n"
                )

            return answer if answer else "No results found."

        except Exception as e:
            return f"Search Error: {e}"
