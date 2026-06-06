from openai import OpenAI


class OpenAIClient:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    def ask(self, question):

        response = self.client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]

        )

        return response.choices[0].message.content