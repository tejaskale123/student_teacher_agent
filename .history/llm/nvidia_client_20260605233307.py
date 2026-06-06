from openai import OpenAI


class NvidiaClient:

    def __init__(self, api_key):

        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )

    def ask(self, question):

        completion = self.client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return completion.choices[0].message.content
