from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class ReflectionAgent:

    def __init__(self):

        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def review(self, answer):

        prompt = f"""
You are a quality reviewer.

Review the answer below.

If the answer is already good,
return it unchanged.

Otherwise improve it.

Answer:

{answer}
"""

        return self.llm.ask(prompt)