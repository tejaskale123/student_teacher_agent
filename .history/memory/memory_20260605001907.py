import json


class Memory:

    def __init__(self):

        self.file_path = "data/chat_history.json"

        self.chat_history = self.load_history()

    def load_history(self):

        try:

            with open(self.file_path, "r") as file:

                return json.load(file)

        except:

            return []

    def save(self, role, message):

        self.chat_history.append(
            {
                "role": role,
                "message": message
            }
        )

        self.save_history()

    def save_history(self):

        with open(self.file_path, "w") as file:

            json.dump(
                self.chat_history,
                file,
                indent=4
            )

    def get_history(self):

        return self.chat_history