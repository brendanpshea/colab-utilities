import csv
import requests
import random
import textwrap

def read_questions(url):
    """Fetches and parses a CSV file of questions from the specified URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        lines = response.text.strip().split('\n')
        reader = csv.reader(lines)
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

    score = 0
    total_questions = len(questions)
    random.shuffle(questions)  # Randomize question order

    for question, correct_answer in questions:
        print(f"\nQuestion {questions.index((question, correct_answer)) + 1} of {total_questions}:")
        user_answer = ask_question(question)

        if user_answer == 'quit':
            print("\nQuitting the quiz.")
            break

        if user_answer == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. {question} is {correct_answer.upper()}.")

    # Displaying the final score
    print(f"\nYou answered {score} out of {total_questions} questions correctly.")
