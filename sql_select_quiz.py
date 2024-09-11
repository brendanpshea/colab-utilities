import sqlite3
import pandas as pd
import requests
import tempfile
import json
from IPython.display import display, HTML, clear_output
from ipywidgets import Textarea, Button, VBox, Layout

def get_table_schemas(conn):
    """
    Retrieves the schema information for all tables in the database.

    Args:
        conn (sqlite3.Connection): The database connection object.

    Returns:
        list: A list of tuples containing table names and their respective column information.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schemas = []
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schemas.append((table_name, columns))
    return schemas

def render_table_schemas(schemas):
    """
    Renders the database schema information in a compact format with HTML formatting.

    Args:
        schemas (list): A list of tuples containing table names and their respective column information.

    Returns:
        str: The rendered HTML string representing the database schema.
    """
    schema_html = "<h2>Database Schema:</h2>"
    schema_html += "<ol>"
    for table_name, columns in schemas:
        column_info = ", ".join(f"{column[1]} {column[2]}" for column in columns)
        schema_html += f"<li><b>{table_name}</b> ({column_info})</li>"
    schema_html += "</ol>"

    schema_html += "<h3>Sample queries</h3>"
    sample_query = f'\"SELECT * FROM {schemas[0][0]}" returns all rows and columns from {schemas[0][0]}.'
    schema_html += sample_query + "<br>"
    sample_query = f'\"SELECT {schemas[0][1][1][1]} FROM {schemas[0][0]}" selects a specific column.'
    schema_html += sample_query
    return schema_html

def validate_questions(conn, answers):
    """
    Validates each answer query to ensure it is executable and a SELECT statement.

    Args:
        conn (sqlite3.Connection): The database connection object.
        answers (list): A list of SQL queries representing the answers to the questions.

    Returns:
        tuple: A tuple containing a boolean indicating if all queries are valid and a list of valid queries.
    """
    valid_queries = []
    for i, query in enumerate(answers, start=1):
        try:
            if not query.strip().lower().startswith('select'):
                raise ValueError(f"Query {i} is not a SELECT statement.")
            conn.execute(query)
            valid_queries.append(query)
        except Exception as e:
            display(HTML(f"<div style='color: red;'>Error in query {i}: {e}</div>"))
            return False, []
    return True, valid_queries

def sql_select_quiz(db_path, questions, answers):
    """
    Iterates through a list of SQL SELECT questions, allowing the user to submit queries
    against a provided SQLite database. Shows results and requires correct answers before proceeding.

    Args:
        db_path (str): Path to the SQLite database file.
        questions (list): List of question prompts.
        answers (list): List of correct SQL queries corresponding to each question.
    """
    if not questions or not answers or len(questions) != len(answers):
        display(HTML("<div>Please provide an equal number of questions and answers.</div>"))
        return

    with sqlite3.connect(db_path) as conn:
        valid, valid_answers = validate_questions(conn, answers)
        if not valid:
            display(HTML("<div>Please correct the errors in your SQL queries before proceeding.</div>"))
            return

        question_index = 0

        def display_current_question():
            """
            Displays the current question and resets the UI for answer submission.
            """
            clear_output(wait=True)
            schemas = get_table_schemas(conn)
            display(HTML(render_table_schemas(schemas)))
            question_html = f"<h3>SQL Question {question_index + 1}:</h3><p>{questions[question_index]}</p>"
            display(HTML(question_html))
            
            text_area.value = ''
            submit_button.layout.visibility = 'visible'
            next_button.layout.visibility = 'hidden'
            retry_button.layout.visibility = 'hidden'
            display(query_widget)

            

        def submit_query(button):
        """
        Handles the submission of the user's query and compares it to the correct answer.
        """
        user_query = text_area.value.strip()  # Remove leading/trailing whitespace

        if not user_query.lower().startswith('select'):
            clear_output(wait=True)  # Clear the old output
            display(HTML(render_table_schemas(get_table_schemas(conn))))  # Display the schema again
            display(HTML(f"<h3>SQL Question {question_index + 1}:</h3><p>{questions[question_index]}</p>"))  # Display the question
            display(query_widget)  # Display the query widget
            display(HTML("<div style='color: red;'><strong>Error:</strong> Please enter a valid SELECT query.</div>"))
            return
        try:
            user_query = text_area.value
            user_result = pd.read_sql_query(user_query, conn)
            correct_query = answers[question_index]
            correct_result = pd.read_sql_query(correct_query, conn)

            clear_output(wait=True)  # Clear the old output
            display(HTML(render_table_schemas(get_table_schemas(conn))))  # Display the schema again
            display(HTML(f"<h3>SQL Question {question_index + 1}:</h3><p>{questions[question_index]}</p>"))  # Display the question
            display(query_widget)  # Display the query widget

            # Add row and column count information
            user_rows, user_cols = user_result.shape
            correct_rows, correct_cols = correct_result.shape
            count_info = f"<div>Your query yielded {user_rows} rows and {user_cols} columns. The expected result had {correct_rows} rows and {correct_cols} columns.</div>"
            display(HTML(count_info))

            if user_result.equals(correct_result):
                feedback = "<div style='color: green;'><strong>Correct!</strong> Your query produced the expected result.</div>"
                submit_button.layout.visibility = 'hidden'
                next_button.layout.visibility = 'visible'
            else:
                feedback = "<div style='color: red;'><strong>Incorrect.</strong> Please try again.</div>"
                submit_button.layout.visibility = 'visible'
                next_button.layout.visibility = 'hidden'
            display(HTML(feedback))

            display(HTML("<h4>Your Results (first five):</h4>"))
            display(user_result.head())
            display(HTML("<h4>Expected Results (first five):</h4>"))
            display(correct_result.head())

        except Exception as e:
            clear_output(wait=True)  # Clear the old output
            display(HTML(render_table_schemas(get_table_schemas(conn))))  # Display the schema again
            display(HTML(f"<h3>SQL Question {question_index + 1}:</h3><p>{questions[question_index]}</p>"))  # Display the question
            display(query_widget)  # Display the query widget
            display(HTML(f"<div>Error executing your query: {str(e)}</div>"))


        def next_question(button):
            """
            Advances to the next question if available.
            """
            nonlocal question_index
            question_index += 1
            if question_index < len(questions):
                display_current_question()
            else:
                submit_button.layout.visibility = 'hidden'
                next_button.layout.visibility = 'hidden'
                retry_button.layout.visibility = 'hidden'
                display(HTML("<div>All questions completed. Well done!</div>"))

        def retry_question(button):
            """
            Resets the interface for the user to retry the current question.
            """
            display_current_question()

        text_area = Textarea(value='', placeholder='Type your SQL query here...', description='Query:', layout=Layout(width='60%', height='100px'))
        submit_button = Button(description="Submit")
        next_button = Button(description="Next Question", layout=Layout(visibility='hidden'))
        retry_button = Button(description="Retry", layout=Layout(visibility='hidden'))

        submit_button.on_click(submit_query)
        next_button.on_click(next_question)
        retry_button.on_click(retry_question)

        query_widget = VBox([text_area, submit_button, retry_button, next_button])

        display_current_question()

def sql_select_quiz_from_id(quiz_id="books"):
    if quiz_id == "books":
        db_url = "https://github.com/brendanpshea/database_sql/raw/main/data/sci_fi_books.db"
        json_url = "https://github.com/brendanpshea/database_sql/raw/main/quiz/sql_book_quiz.json"
    sql_select_quiz_url(db_url,json_url)
        
def sql_select_quiz_url(db_url, json_url):
    """
    Launches the SQL SELECT quiz using the provided database and JSON URLs.

    Args:
        db_url (str): URL of the SQLite database file.
        json_url (str): URL of the JSON file containing questions and answers.
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_db:
        db_path = temp_db.name
        response = requests.get(db_url)
        temp_db.write(response.content)

    response = requests.get(json_url)
    quiz_data = json.loads(response.text)

    questions = [item['question'] for item in quiz_data]
    answers = [item['answer'] for item in quiz_data]

    sql_select_quiz(db_path, questions, answers)
