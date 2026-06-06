from llm.openai_client import OpenAIClient
from config import OPENAI_API_KEY

client = OpenAIClient(OPENAI_API_KEY)

response = client.ask("What is AI?")

print(response)