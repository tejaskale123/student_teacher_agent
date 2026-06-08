from openai import OpenAI


class NvidiaClient:

    def __init__(self, api_key):

        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
            timeout=120
        )

    def ask(self, question):

        print("Sending request to NVIDIA...")

        completion = self.client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.2,
           max_tokens=400
        )

        print("Response received!")

        return completion.choices[0].message.content