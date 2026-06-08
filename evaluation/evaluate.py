import time
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


QUESTIONS = [
    "2 + 2",
    "10 * 5",
    "100 / 4",
    "search latest python news",
    "latest ai news",
    "find machine learning news",
    "lookup python release news",
    "search latest data science news",
    "summarize pdf",
    "explain chapter from pdf",
    "what is in the document",
    "summary of notes",
    "compare python functions from pdf with latest python news",
    "compare chapter 1 with latest ai news",
    "difference between pdf notes and latest news",
    "what is a function in python",
    "explain loops",
    "what is a variable",
    "teach me lists",
    "explain dictionaries",
    "how does recursion work",
    "what is oop",
    "explain classes",
    "what is inheritance",
    "what is polymorphism",
    "latest technology news",
    "search latest programming news",
    "find latest software news",
    "lookup latest education news",
    "search python tutorials",
    "compare pdf summary with latest technology news",
    "compare notes with latest programming news",
    "difference between document and latest ai news",
    "summarize chapter 2",
    "pdf key points",
    "document main ideas",
    "notes summary",
    "3 * (4 + 5)",
    "50 - 17",
    "8 / 2 + 6",
    "what is python",
    "explain modules",
    "what is pip",
    "what is an api",
    "teach me error handling",
    "explain file handling",
    "latest open source news",
    "search latest developer news",
    "compare python functions from pdf with latest developer news",
    "summarize pdf and compare with latest news",
]


def main():
    from agents.teacher_agent import TeacherAgent

    teacher = TeacherAgent()
    total_time = 0
    successes = 0

    for question in QUESTIONS:
        started_at = time.perf_counter()

        try:
            answer = teacher.answer(question)
            success = bool(str(answer).strip())
        except Exception as error:
            answer = f"ERROR: {error}"
            success = False

        elapsed = time.perf_counter() - started_at
        total_time += elapsed
        successes += int(success)

        print(f"QUESTION: {question}")
        print(f"SUCCESS: {success}")
        print(f"TIME: {elapsed:.2f} sec")
        print(f"ANSWER PREVIEW: {str(answer)[:200]}")
        print("-" * 60)

    total = len(QUESTIONS)
    print("EVALUATION SUMMARY")
    print(f"QUESTIONS: {total}")
    print(f"SUCCESS RATE: {(successes / total) * 100:.2f}%")
    print(f"AVERAGE RESPONSE TIME: {total_time / total:.2f} sec")


if __name__ == "__main__":
    main()
