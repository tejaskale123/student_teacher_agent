from tools.search_tool import SearchTool


class SearchAgent:

    def __init__(self):
        self.search_tool = SearchTool()

    def run(self, question):
        return self.search_tool.search(question)