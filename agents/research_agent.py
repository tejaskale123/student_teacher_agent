from agents.search_agent import SearchAgent


class ResearchAgent:

    def __init__(self):

        self.search_agent = SearchAgent()

    def research(self, topic):

        result = self.search_agent.run(topic)

        return f"""
RESEARCH REPORT

Topic:
{topic}

Findings:
{result}
"""