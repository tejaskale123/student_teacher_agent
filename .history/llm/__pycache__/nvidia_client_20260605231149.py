import requests


class NvidiaClient:

    def __init__(self, api_key):

        self.api_key = api_key

    def ask(self, question):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "temperature": 0.7,
            "top_p": 1,
            "max_tokens": 500,
            "model": "meta/llama-3.1-8b-instruct"
        }

        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        return response.json()