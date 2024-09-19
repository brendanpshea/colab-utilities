import sqlite3
import pandas as pd
import requests
import tempfile
import json
from IPython.display import display, HTML, clear_output
from ipywidgets import (Textarea, Button, VBox, HBox, Layout, IntProgress, 
                        Tab, IntText, Label, Box, HTML as HTMLWidget)

def get_table_schemas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [(table[0], cursor.execute(f"PRAGMA table_info({table[0]})").fetchall()) 
            for table in cursor.fetchall()]

def render_table_schemas(schemas):
    schema_html = "<h3>Database Schema:</h3><ul>"
    for table_name, columns in schemas:
        column_info = ", ".join(f"{column[1]} {column[2]}" for column in columns)
        schema_html += f"<li><b>{table_name}</b> ({column_info})</li>"
    schema_html += "</ul>"
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
        self.progress_bar = IntProgress(min=0, max=len(self.questions), value=1, description='Progress:')
        self.question_label = HTMLWidget(value='')
        
        self.text_area = Textarea(placeholder='Type your SQL query here...', 
                                  layout=Layout(width='100%', height='150px'))
        self.submit_button = Button(description="Submit", button_style='success')
        self.clear_button = Button(description="Clear", button_style='warning')
        self.hint_button = Button(description="Hint", button_style='info')
        
        self.skip_input = IntText(value=1, min=1, max=len(self.questions), layout=Layout(width='60px'))
        self.skip_button = Button(description="Skip to", button_style='info')
        self.skip_box = HBox([Label('Go to question:'), self.skip_input, self.skip_button])

        self.submit_button.on_click(self.submit_query)
        self.clear_button.on_click(self.clear_query)
        self.skip_button.on_click(self.skip_to_question)
        self.hint_button.on_click(self.show_hint)

        self.query_box = VBox([self.text_area, 
                               HBox([self.submit_button, self.clear_button, self.hint_button]),
                               self.skip_box])
        
        self.results_area = HTMLWidget(value='')
        self.try_again_button = Button(description="Try Again", button_style='warning')
        self.next_button = Button(description="Next Question", button_style='info')
        self.try_again_button.on_click(self.try_again)
        self.next_button.on_click(self.next_question)
        
        self.results_box = VBox([self.results_area, HBox([self.try_again_button, self.next_button])])
        
        self.tab = Tab(children=[self.query_box, self.results_box])
        self.tab.set_title(0, 'Query')
        self.tab.set_title(1, 'Results')
        
        self.main_box = VBox([self.progress_bar, self.question_label, self.tab])

    def display_current_question(self, _=None):
        clear_output(wait=True)
        schemas = get_table_schemas(self.conn)
        self.question_label.value = (f"<h3>Question {self.current_index + 1} of {len(self.questions)}:</h3>"
                                     f"<p>{self.questions[self.current_index]}</p>"
                                     f"{render_table_schemas(schemas)}")
        
        self.text_area.value = ''
        self.submit_button.disabled = False
        self.skip_input.max = len(self.questions)
        self.progress_bar.value = self.current_index + 1
        self.tab.selected_index = 0  # Switch to Query tab
        display(self.main_box)

    def submit_query(self, _):
        user_query = self.text_area.value.strip()
        if not user_query.lower().startswith('select'):
            self.display_error("Please enter a valid SELECT query.")
            return

        try:
            user_result = execute_query(self.conn, user_query)
            correct_result = execute_query(self.conn, self.answers[self.current_index])
            self.display_results(user_result, correct_result)
        except ValueError as e:
            self.display_error(str(e))

    def display_results(self, user_result, correct_result):
        user_rows, user_cols = user_result.shape
        correct_rows, correct_cols = correct_result.shape
        count_info = (f"<p>Your query yielded {user_rows} rows and {user_cols} columns. "
                      f"The expected result had {correct_rows} rows and {correct_cols} columns.</p>")
        
        if user_result.equals(correct_result):
            feedback = "<h3 style='color: green;'>Correct! Your query produced the expected result.</h3>"
            self.next_button.disabled = False
            self.try_again_button.disabled = True
        else:
            feedback = "<h3 style='color: red;'>Incorrect. Please try again.</h3>"
            self.next_button.disabled = True
            self.try_again_button.disabled = False

        results_html = feedback + count_info
        results_html += "<h4>Your Results (first five rows):</h4>"
        results_html += user_result.head().to_html()
        results_html += "<h4>Expected Results (first five rows):</h4>"
        results_html += correct_result.head().to_html()
        
        self.results_area.value = results_html
        self.tab.selected_index = 1  # Switch to Results tab

    def display_error(self, message):
        self.results_area.value = f"<h3 style='color: red;'>Error: {message}</h3>"
        self.tab.selected_index = 1  # Switch to Results tab

    def clear_query(self, _):
        self.text_area.value = ''

    def try_again(self, _):
        self.tab.selected_index = 0  # Switch back to Query tab

    def next_question(self, _):
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.display_current_question()
        else:
            self.main_box.children = [HTMLWidget(value="<h2>All questions completed. Well done!</h2>")]
            display(self.main_box)

    def skip_to_question(self, _):
        new_index = self.skip_input.value - 1
        if 0 <= new_index < len(self.questions):
            self.current_index = new_index
            self.display_current_question()
        else:
            self.display_error(f"Invalid question number. Please enter a number between 1 and {len(self.questions)}.")

    def show_hint(self, _):
        correct_query = self.answers[self.current_index]
        words = correct_query.split()
        hint = []
        for i, word in enumerate(words):
            if i % 2 == 0:
                hint.append(word)
            else:
                hint.append('____' * (len(word) // 4 + 1))  # Adjust underscores based on word length
        hint = " ".join(hint)
        self.results_area.value = f"<h3>Hint:</h3><p>{hint}</p>"
        self.tab.selected_index = 1  # Switch to Results tab
def sql_select_quiz_from_id(quiz_id="books"):
    if quiz_id == "books":
        db_url = "https://github.com/brendanpshea/database_sql/raw/main/data/sci_fi_books.db"
        json_url = "https://github.com/brendanpshea/database_sql/raw/main/quiz/sql_book_quiz.json"
    elif quiz_id == "movies":
        db_url = "https://github.com/brendanpshea/database_sql/raw/main/data/movie.sqlite"
        json_url = "https://github.com/brendanpshea/database_sql/raw/main/quiz/sql_movie_quiz.json" 
    elif quiz_id == "mario":
        db_url = "https://github.com/brendanpshea/database_sql/raw/main/data/mario_bros_plumbing.db"
        json_url = "https://github.com/brendanpshea/database_sql/raw/main/quiz/sql_mario_quiz.json"  
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
