import csv
import random
import sys
import requests

def convert_answer(answer):
    answer = answer.strip().lower()
    if answer in ['true', 't', '1', 'yes', 'y']:
        return '1'
    elif answer in ['false', 'f', '0', 'no', 'n']:
        return '0'
    else:
        return None

def validate_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 2:
                    return False
                if convert_answer(row[1]) is None:
                    return False
        return True
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except Exception as e:
        print(f"An error occurred while validating the CSV file: {str(e)}")
        return False

def load_questions_from_file(file_path):
    questions = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row_num, row in enumerate(reader, start=1):
                if len(row) != 2:
                    print(f"Invalid format in CSV file at line {row_num}: {row}")
                    continue
                question = row[0]
                answer = convert_answer(row[1])
                if answer is None:
                    print(f"Missing or invalid answer in CSV file at line {row_num}: {row}")
                    continue
                questions.append((question, bool(int(answer))))
        return questions
    except Exception as e:
        print(f"An error occurred while loading questions from the file: {str(e)}")
        return []

def load_questions_from_url(url):
    questions = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.text
        reader = csv.reader(csv_data.splitlines())
        for row_num, row in enumerate(reader, start=1):
            if len(row) != 2:
                print(f"Invalid format in CSV data from URL at line {row_num}: {row}")
                continue
            question = row[0]
            answer = convert_answer(row[1])
            if answer is None:
                print(f"Missing or invalid answer in CSV data from URL at line {row_num}: {row}")
                continue
            questions.append((question, bool(int(answer))))
        return questions
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while loading questions from the URL: {str(e)}")
        return []
    except Exception as e:
        print(f"An error occurred while processing the CSV data from the URL: {str(e)}")
        return []

def run_quiz(questions):
    score = 0
    total_questions = len(questions)
    random.shuffle(questions)

    for i, (question, answer) in enumerate(questions, start=1):
        print(f"\nQuestion {i} of {total_questions}: {question}")
        user_answer = input("Enter your answer (T/F) or 'Q' to quit: ").upper()

        while user_answer not in ['T', 'F', 'TRUE', 'FALSE', 'Q']:
            user_answer = input("Invalid input. Please enter 'T', 'F', 'TRUE', 'FALSE', or 'Q' to quit: ").upper()

        if user_answer == 'Q':
            print("\nQuiz aborted.")
            print_summary(score, i - 1, total_questions)
            return

        user_answer = user_answer in ['T', 'TRUE']

        if user_answer == answer:
            print("Correct!")
            score += 1
        else:
            print("Incorrect!")

    print("\nQuiz completed!")
    print_summary(score, total_questions, total_questions)

def print_summary(score, questions_answered, total_questions):
    print(f"\nQuiz Summary:")
    print(f"Questions Answered: {questions_answered}/{total_questions}")
    print(f"Correct Answers: {score}")
    print(f"Incorrect Answers: {questions_answered - score}")
    percentage = (score / questions_answered) * 100 if questions_answered > 0 else 0
    print(f"Percentage: {percentage:.2f}%")

def run_quiz_local(csv_file_path):
    if not validate_csv(csv_file_path):
        print("Invalid CSV file format. Please ensure the file has two columns and the second column contains valid answers.")
        return

    questions = load_questions_from_file(csv_file_path)
    if not questions:
        print("No questions loaded from the CSV file.")
        return

    run_quiz(questions)

def run_quiz_url(url):
    questions = load_questions_from_url(url)
    if not questions:
        print("No questions loaded from the URL.")
        return

    run_quiz(questions)
