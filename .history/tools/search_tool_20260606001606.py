from duckduckgo_search import DDGS


class SearchTool:

    def search(self, query):

        try:

            with DDGS() as ddgs:

                results = list(
                    ddgs.text(
                        query,
                        max_results=5
                    )
                )

            answer = ""

            for i, result in enumerate(results, start=1):

                answer += (
                    f"{i}. {result['title']}\n"
                    f"{result['href']}\n\n"
                )

            return answer

        except Exception as e:

            return f"Search Error: {e}"