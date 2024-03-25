import csv
import random
import sys
import requests
from IPython.display import display, HTML
import ipywidgets as widgets

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

    def check_answer(answer):
        nonlocal score, i
        if answer == 'Q':
            display(HTML("<p>Quiz aborted.</p>"))
            print_summary(score, i - 1, total_questions)
            return
        user_answer = answer == 'T'
        if user_answer == questions[i-1][1]:
            display(HTML("<p style='color: green;'>Correct!</p>"))
            score += 1
        else:
            display(HTML("<p style='color: red;'>Incorrect!</p>"))
        i += 1
        if i <= total_questions:
            ask_question()
        else:
            display(HTML("<h3>Quiz completed!</h3>"))
            print_summary(score, total_questions, total_questions)

    def ask_question():
        display(HTML(f"<h3>Question {i} of {total_questions}:</h3>"))
        display(HTML(f"<p>{questions[i-1][0]}</p>"))
        true_button = widgets.Button(description='True')
        false_button = widgets.Button(description='False')
        quit_button = widgets.Button(description='Quit')
        true_button.on_click(lambda _: check_answer('T'))
        false_button.on_click(lambda _: check_answer('F'))
        quit_button.on_click(lambda _: check_answer('Q'))
        display(widgets.HBox([true_button, false_button, quit_button]))

    i = 1
    ask_question()

def print_summary(score, questions_answered, total_questions):
    percentage = (score / questions_answered) * 100 if questions_answered > 0 else 0
    summary_html = f"""
    <h3>Quiz Summary:</h3>
    <ul>
        <li>Questions Answered: {questions_answered}/{total_questions}</li>
        <li>Correct Answers: {score}</li>
        <li>Incorrect Answers: {questions_answered - score}</li>
        <li>Percentage: {percentage:.2f}%</li>
    </ul>
    """
    display(HTML(summary_html))

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
