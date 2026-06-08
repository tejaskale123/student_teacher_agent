class CombinerAgent:

    def combine(self, results):

        output = []

        for name, result in results.items():

            output.append(
                f"{name.upper()} RESULT:\n{result}"
            )

        return "\n\n".join(output)