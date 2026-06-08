from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class FormatterAgent:

    def __init__(self):

        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def format(self, answer):

        prompt = f"""
You are an expert AI teacher.

Format the answer professionally.

Rules:

0. NEVER invent information.

0.1 Use ONLY information present in the answer.

0.2 If answer contains:

PDF Findings
Search Findings

Then preserve those sections exactly in meaning and keep the comparison structure.

0.3 Do not change the topic.

0.4 Do not replace comparison topics.

0.5 Do not add outside facts, version numbers, release names, dates, examples, or corrections.

0.6 If the input says Python functions from PDF and Python news from search, do not turn it into a Python version comparison.

0.7 If a section already exists, improve formatting only. Do not rewrite its factual meaning.

0.8 If answer contains:

SEARCH RESULT:
and
RAG RESULT:

ALWAYS create:

# Comparison Report

## PDF Findings

## Search Findings

## Similarities

## Differences

## Final Conclusion

Do not use normal format for comparison answers.

0.9 Never rename comparison topics.

0.10 If PDF discusses functions and Search discusses news, keep those exact topics.

1. Create title.

2. Add:

## Summary

## Key Points

## Detailed Explanation

## Example

## Conclusion

3. If comparison:

Use:

# Comparison Report

## PDF Findings

## Search Findings

## Similarities

## Differences

## Final Conclusion

For comparison answers, use ONLY the comparison format above.
Do not add ## Summary, ## Key Points, ## Detailed Explanation, ## Example, or ## Conclusion to comparison answers.

4. Use bullet points.

5. Keep URLs.

6. Make answer look like ChatGPT.

7. If there is not enough information for ## Example, write a very short example only from the answer. If no example is supported, omit ## Example.

Answer:

{answer}
"""

        return self.llm.ask(prompt)
