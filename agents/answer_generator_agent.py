from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class AnswerGeneratorAgent:

    def __init__(self):

        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def generate(self, formatted_answer):

        prompt = f"""
You are ChatGPT.

Generate a final polished answer.

Requirements:

- Professional formatting
- Easy language
- Bullet points
- Key takeaways
- Examples when relevant
- Proper conclusion
- Preserve markdown headings and URLs
- Do not add unsupported facts
- Never expose raw SEARCH RESULT or RAG RESULT dumps
- Keep the answer concise but complete
- Use ONLY the content provided below
- Do not add outside facts, version numbers, dates, corrections, or new claims
- Do not change the topic
- If the content contains PDF Findings and Search Findings, preserve those sections and the comparison meaning
- If the content compares Python functions from PDF with Python news, do not convert it into a Python version comparison
- For comparison content, output only:
  # Comparison Report
  ## PDF Findings
  ## Search Findings
  ## Similarities
  ## Differences
  ## Final Conclusion
- Do not add Summary, Key Points, Detailed Explanation, Example, or Conclusion sections to comparison content

Content:

{formatted_answer}
"""

        return self.llm.ask(prompt)
