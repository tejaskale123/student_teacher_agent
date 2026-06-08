class CombinerAgent:

    def combine(self, results):

        output = []

        for name, result in results.items():

            output.append(
                f"{name.upper()} RESULT:\n{result}"
            )

        combined_text = "\n\n".join(output)

        print("\n=== COMBINED ===")
        print(combined_text)

        return combined_text
