from tools.search_tool import SearchTool
from agents.query_rewriter_agent import QueryRewriterAgent


class SearchAgent:

    def __init__(self):
        self.search_tool = SearchTool()
        self.query_rewriter = QueryRewriterAgent()

    def run(self, question):
        print("SEARCH START")

        question = (
            self.query_rewriter
            .rewrite(
                question
            )
        )

        print("SEARCH QUERY:", question)

        result = self.search_tool.search(question)

        print("\n=== SEARCH RESULT ===")
        print(result[:300])

        return result
