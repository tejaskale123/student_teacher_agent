from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class ReflectionAgent:

    def __init__(self):

        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def review(self, search_result, rag_result, combined_result=None):

        evidence = combined_result or f"""
SEARCH RESULT:

{search_result}

PDF RESULT:

{rag_result}
"""

        prompt = f"""
You are a strict evidence-based comparison agent.

Use the evidence below to create a clean comparison answer.

Evidence:

{evidence}

Create exactly these sections:

# Comparison Report

## PDF Findings

## Search Findings

## Similarities

## Differences

## Final Conclusion

Rules:

- Do not return raw search dumps.
- Preserve useful URLs.
- Do not invent facts that are not in the evidence.
- Use PDF RESULT only for PDF Findings.
- Use SEARCH RESULT only for Search Findings.
- Do not change the topic.
- Do not compare Python versions unless the evidence is specifically about Python versions.
- If evidence is about Python functions and Python news, compare fundamentals from the PDF with updates/resources from search.
- Return structured markdown.
"""

        return self.llm.ask(prompt)
