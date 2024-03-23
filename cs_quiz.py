import csv
import requests
import random
import textwrap

def read_questions(url):
    """Fetches and parses a CSV file of questions from the specified URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure a successful request
        lines = response.text.strip().split('\n')
        reader = csv.reader(lines)
        # Store each question and its answer as a tuple in a list
        questions = [(row[0], row[1].lower()) for row in reader if len(row) == 2]
        return questions
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the CSV file: {e}")
        return []
    except csv.Error as e:
        print(f"Error parsing the CSV file: {e}")
        return []

def ask_question(question):
    """Displays the question and prompts for an answer, ensuring valid input."""
    wrapped_question = textwrap.fill(question, width=80)
    while True:
        user_answer = input(f"{wrapped_question} (True/False/Quit): ").lower()
        if user_answer in ['true', 'false', 'quit']:
            return user_answer
        else:
            print("Invalid input. Please enter 'True', 'False', or 'Quit'.")

def cs_quiz(url):
    """Conducts a quiz by asking questions from a CSV file fetched from a URL."""
    questions = read_questions(url)
    if not questions:
        print("No questions found. Exiting the quiz.")
        return

    random.shuffle(questions)  # Randomize question order

    for i, (question, correct_answer) in enumerate(questions, 1), total=len(questions):
        print(f"\nQuestion {i} of {total}:")
        user_answer = ask_question(question)

        if user_answer == 'quit':
            print("\nQuitting the quiz.")
            break

        if user_answer == correct_answer:
            print("Correct!")
        else:
            print(f"Incorrect. {question} is {correct_answer.upper()}.")

    # Summary is omitted as no calculation or display of score is required per instructions
