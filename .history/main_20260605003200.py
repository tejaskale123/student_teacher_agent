from agents.student_agent import StudentAgent

def main():

    print("=== Student Teacher Agent ===")

    student = StudentAgent()

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        response = student.ask_teacher(question)

        print(f"\nTeacher: {response}")

        print("\nMemory:")
       #S print(student.teacher.memory.get_history())


if __name__ == "__main__":
    main()