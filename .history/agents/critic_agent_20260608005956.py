from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class CriticAgent:

    def __init__(self):

        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def critique(self, answer):

        prompt = f"""
You are a critic agent.

Review this answer.

Check:

1. Accuracy
2. Completeness
3. Clarity

If needed improve it.

Answer:

{answer}
"""

        return self.llm.ask(prompt)