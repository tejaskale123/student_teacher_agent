class SupervisorAgent:

    def route(self, query):

        if is_math(query):
            return math_agent.run(query)

        elif is_search(query):
            return search_agent.run(query)

        elif is_pdf(query):
            return rag_agent.run(query)

        else:
            return teacher_agent.run(query)