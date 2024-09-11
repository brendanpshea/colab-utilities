import sqlite3
import pandas as pd
import requests
import tempfile
import json
from IPython.display import display, HTML, clear_output
from ipywidgets import Textarea, Button, VBox, Layout, HBox, IntText

def get_table_schemas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [(table[0], cursor.execute(f"PRAGMA table_info({table[0]})").fetchall()) 
            for table in cursor.fetchall()]

def render_table_schemas(schemas):
    schema_html = "<h2>Database Schema:</h2><ol>"
    for table_name, columns in schemas:
        column_info = ", ".join(f"{column[1]} {column[2]}" for column in columns)
        schema_html += f"<li><b>{table_name}</b> ({column_info})</li>"
    schema_html += "</ol>"
    schema_html += f"<h3>Sample queries</h3>"
    schema_html += f'"SELECT * FROM {schemas[0][0]}" returns all rows and columns from {schemas[0][0]}.<br>'
    schema_html += f'"SELECT {schemas[0][1][0][1]} FROM {schemas[0][0]}" selects a specific column.'
    return schema_html

def execute_query(conn, query):
    try:
        return pd.read_sql_query(query, conn)
    except Exception as e:
        raise ValueError(f"Error executing query: {str(e)}")

class SQLQuiz:
    def __init__(self, db_path, questions, answers):
        self.conn = sqlite3.connect(db_path)
        self.questions = questions
        self.answers = answers
        self.current_index = 0
        self.setup_ui()

    def setup_ui(self):
        self.text_area = Textarea(placeholder='Type your SQL query here...', 
                                  description='Query:', 
                                  layout=Layout(width='60%', height='100px'))
        self.submit_button = Button(description="Submit")
        self.next_button = Button(description="Next Question", 
                                  layout=Layout(visibility='hidden'))
        self.retry_button = Button(description="Retry", 
                                   layout=Layout(visibility='hidden'))
        
        # New UI elements for skipping to a specific question
        self.skip_input = IntText(value=1, min=1, max=len(self.questions), description='Question:')
        self.skip_button = Button(description="Skip to")
        self.skip_box = HBox([self.skip_input, self.skip_button])

        self.submit_button.on_click(self.submit_query)
        self.next_button.on_click(self.next_question)
        self.retry_button.on_click(self.display_current_question)
        self.skip_button.on_click(self.skip_to_question)

        self.query_widget = VBox([self.text_area, self.submit_button, 
                                  self.retry_button, self.next_button, self.skip_box])

    def display_current_question(self, _=None):
        clear_output(wait=True)
        schemas = get_table_schemas(self.conn)
        display(HTML(render_table_schemas(schemas)))
        display(HTML(f"<h3>SQL Question {self.current_index + 1}:</h3>"
                     f"<p>{self.questions[self.current_index]}</p>"))
        
        self.text_area.value = ''
        self.submit_button.layout.visibility = 'visible'
        self.next_button.layout.visibility = 'hidden'
        self.retry_button.layout.visibility = 'hidden'
        self.skip_input.max = len(self.questions)
        display(self.query_widget)

    def submit_query(self, _):
        user_query = self.text_area.value.strip()
        if not user_query.lower().startswith('select'):
            self.display_error("Please enter a valid SELECT query.")
            return

        try:
            user_result = execute_query(self.conn, user_query)
            correct_result = execute_query(self.conn, self.answers[self.current_index])

            self.display_current_question()
            self.display_results(user_result, correct_result)
        except ValueError as e:
            self.display_error(str(e))

    def display_results(self, user_result, correct_result):
        user_rows, user_cols = user_result.shape
        correct_rows, correct_cols = correct_result.shape
        count_info = (f"<div>Your query yielded {user_rows} rows and {user_cols} columns. "
                      f"The expected result had {correct_rows} rows and {correct_cols} columns.</div>")
        display(HTML(count_info))

        if user_result.equals(correct_result):
            self.display_feedback(True)
        else:
            self.display_feedback(False)

        display(HTML("<h4>Your Results (first five):</h4>"))
        display(user_result.head())
        display(HTML("<h4>Expected Results (first five):</h4>"))
        display(correct_result.head())

    def display_feedback(self, is_correct):
        if is_correct:
            feedback = "<div style='color: green;'><strong>Correct!</strong> Your query produced the expected result.</div>"
            self.submit_button.layout.visibility = 'hidden'
            self.next_button.layout.visibility = 'visible'
        else:
            feedback = "<div style='color: red;'><strong>Incorrect.</strong> Please try again.</div>"
            self.submit_button.layout.visibility = 'visible'
            self.next_button.layout.visibility = 'hidden'
        display(HTML(feedback))

    def display_error(self, message):
        self.display_current_question()
        display(HTML(f"<div style='color: red;'><strong>Error:</strong> {message}</div>"))

    def next_question(self, _):
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.display_current_question()
        else:
            self.submit_button.layout.visibility = 'hidden'
            self.next_button.layout.visibility = 'hidden'
            self.retry_button.layout.visibility = 'hidden'
            self.skip_box.layout.visibility = 'hidden'
            display(HTML("<div>All questions completed. Well done!</div>"))

    def skip_to_question(self, _):
        new_index = self.skip_input.value - 1
        if 0 <= new_index < len(self.questions):
            self.current_index = new_index
            self.display_current_question()
        else:
            self.display_error(f"Invalid question number. Please enter a number between 1 and {len(self.questions)}.")

def sql_select_quiz_from_id(quiz_id="books"):
    if quiz_id == "books":
        db_url = "https://github.com/brendanpshea/database_sql/raw/main/data/sci_fi_books.db"
        json_url = "https://github.com/brendanpshea/database_sql/raw/main/quiz/sql_book_quiz.json"
    sql_select_quiz_url(db_url, json_url)

def sql_select_quiz_url(db_url, json_url):
    with tempfile.NamedTemporaryFile(delete=False) as temp_db:
        db_path = temp_db.name
        response = requests.get(db_url)
        temp_db.write(response.content)

    response = requests.get(json_url)
    quiz_data = json.loads(response.text)

    questions = [item['question'] for item in quiz_data]
    answers = [item['answer'] for item in quiz_data]

    quiz = SQLQuiz(db_path, questions, answers)
    quiz.display_current_question()
