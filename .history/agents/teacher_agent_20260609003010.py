import json
import time
from datetime import datetime
from pathlib import Path

from memory.memory import Memory
from tools.calculator_tool import CalculatorTool
from tools.search_tool import SearchTool
from agents.router import Router
from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY
from agents.supervisor_agent import SupervisorAgent
from agents.formatter_agent import FormatterAgent
from agents.answer_generator_agent import AnswerGeneratorAgent
from agents.intent_agent import IntentAgent

class TeacherAgent:

    def __init__(self):
        self.memory = Memory()
        self.calculator = CalculatorTool()
        self.search_tool = SearchTool()
        self.router = Router()
        self.llm = NvidiaClient(NVIDIA_API_KEY)
        self.rag = None
        self.supervisor = SupervisorAgent()
        self.formatter = FormatterAgent()
        self.answer_generator = AnswerGeneratorAgent()
        self.intent = IntentAgent()
        self.last_run = {}

    def log_run(self, payload):
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        with (logs_dir / "agent_runs.jsonl").open("a", encoding="utf-8") as file:
            file.write(
                json.dumps(
                    payload,
                    ensure_ascii=False
                )
            )
            file.write("\n")

    def answer(self, question):
        if not question.strip():
         return "Please enter a question.

        started_at = time.perf_counter()
        self.memory.save("student", question)

        intent = (
            self.intent.detect(
                question
            )
        )

        print(
            "INTENT:",
            intent
        )

        if intent == "short_answer":

            prompt = f"""
Answer shortly.

Question:
{question}

Format:

# Topic

Full Form:
...

Meaning:
...

Use:
...
"""

            result = self.llm.ask(prompt)

            self.memory.save(
                "teacher",
                result
            )

            self.last_run = {
                "query": question,
                "route": "knowledge",
                "agents": ["TeacherAgent", "IntentAgent"],
                "execution_time": round(time.perf_counter() - started_at, 2),
                "retrieved_chunks": "N/A"
            }
            self.log_run(
                {
                    **self.last_run,
                    "timestamp": datetime.now().isoformat(timespec="seconds")
                }
            )

            return result

        route = self.router.route(question)

        if route in ["calculator", "search", "rag", "multi"]:
            result = self.supervisor.handle(
                route,
                question
            )

            self.memory.save(
                "teacher",
                str(result)
            )

            self.last_run = self.supervisor.last_run

            return str(result)

        history = self.memory.get_history()
        context = ""
        for item in history[-5:]:
            context += f"{item['role']}: {item['message']}\n"

        full_prompt = f"""
Previous Conversation:

{context}
Current Question:
{question}

Detected Intent:
{intent}

Answer naturally and use the conversation context if relevant.
If intent is exam, explain in an exam-focused way with definitions, key points, and short-answer style.
If intent is interview, explain with interview questions, practical points, and concise sample answers.
If intent is research, include a deeper structured explanation.
"""

        response = self.llm.ask(full_prompt)
        formatted_response = self.formatter.format(
            response
        )
        final_response = self.answer_generator.generate(
            formatted_response
        )
        self.memory.save("teacher", final_response)
        self.last_run = {
            "query": question,
            "route": route,
            "agents": ["TeacherAgent", "IntentAgent", "FormatterAgent", "AnswerGeneratorAgent"],
            "execution_time": round(time.perf_counter() - started_at, 2),
            "retrieved_chunks": "N/A"
        }
        self.log_run(
            {
                **self.last_run,
                "timestamp": datetime.now().isoformat(timespec="seconds")
            }
        )
        return final_response
