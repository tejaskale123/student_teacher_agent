from ddgs import DDGS


class SearchTool:

    def search(self, query):
        try:
            print("Searching:", query)
            results = DDGS().text(query, max_results=5)

            answer = ""
            for i, result in enumerate(results, start=1):
                answer += f"{i}. {result.get('title', 'No Title')}\n"
                if 'href' in result:
                    answer += f"{result['href']}\n\n"
                elif 'url' in result:
                    answer += f"{result['url']}\n\n"

            return answer if answer else "No results found."

        except Exception as e:
            return f"Search Error: {e}"
