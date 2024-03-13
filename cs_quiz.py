# Allows delivery of CS quizes in Jupyter Notebooks

import csv
import requests
import random
import textwrap

def read_questions(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
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
    # Use the textwrap module to wrap text at 80 characters
    wrapped_question = textwrap.fill(question, width=80)
    while True:
        user_answer = input(f"{wrapped_question} (True/False/Quit): ")
        user_answer = user_answer.lower()
        if user_answer in ['true', 'false', 'quit']:
            return user_answer
        else:
            print("Invalid input. Please enter 'True', 'False', or 'Quit'.")

def cs_quiz(url):
    questions = read_questions(url)
    if not questions:
        print("No questions found. Exiting the quiz.")
        return

    num_questions = len(questions)
    score = 0
    answered_questions = 0

    random.shuffle(questions)  # Randomize the order of questions

    for i, (question, answer) in enumerate(questions, 1):
        print(f"\nQuestion {i} of {num_questions}:")
        user_answer = ask_question(question)

        if user_answer == 'quit':
            print("\nQuitting the quiz.")
            break

        answered_questions += 1
        if user_answer == answer:
            score += 1

    if answered_questions > 0:
        proportion_correct = score / answered_questions
        print(f"\nYou answered {answered_questions} out of {num_questions} questions.")
        print(f"Your score: {score}/{answered_questions} ({proportion_correct:.2%})")
    else:
        print("No questions answered.")
