from rag_chat import RAGChat
import sys
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)
bot = RAGChat()

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    answer = bot.ask(question)

    print("\nAnswer:\n")

    print(answer)