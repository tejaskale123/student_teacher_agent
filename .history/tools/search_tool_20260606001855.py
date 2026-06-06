from duckduckgo_search import DDGS

class SearchTool:

```
def search(self, query):

    try:

        print("Searching:", query)

        with DDGS() as ddgs:

            results = list(ddgs.text(query, max_results=5))

        print(results)

        return str(results)

    except Exception as e:

        return f"ERROR: {e}"
```
