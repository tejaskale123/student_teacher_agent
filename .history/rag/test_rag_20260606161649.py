from rag_chat import RAGChat

bot = RAGChat()

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    answer = bot.ask(question)

    print("\nAnswer:\n")

    print(answer)