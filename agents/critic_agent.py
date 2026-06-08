from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class CriticAgent:

    def __init__(self):

        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def critique(self, answer):
        print("CRITIC RUNNING")

        prompt = f"""
You are a strict evidence-preserving critic agent.

Review the answer for clarity and internal consistency only.

Check:

1. Hallucinations
2. Unsupported claims
3. Completeness
4. Clarity

Rules:

- Use ONLY information already present in the answer.
- NEVER add outside facts, version numbers, dates, corrections, or new examples.
- If a claim is unsupported by the answer, remove it instead of replacing it with outside knowledge.
- Preserve the original topic.
- Preserve these headings if present:
  PDF Findings
  Search Findings
  Similarities
  Differences
  Final Conclusion
- If the answer is already clear, return it unchanged.
- If needed, improve wording only and keep the same useful structure.

Answer:

{answer}
"""

        return self.llm.ask(prompt)
