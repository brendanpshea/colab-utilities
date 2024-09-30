import sqlite3
import pandas as pd
import requests
import tempfile
import json
from abc import ABC, abstractmethod

# For IPython and ipywidgets UI
from IPython.display import display, clear_output
from ipywidgets import (Textarea, Button, VBox, HBox, Layout, IntProgress, 
                        Tab, IntText, Label, HTML as HTMLWidget)


# Abstract base class for Database operations
class DatabaseInterface(ABC):
    @abstractmethod
    def execute_query(self, query):
        pass

    @abstractmethod
    def get_table_schemas(self):
        pass


# SQLite database implementation
class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def execute_query(self, query):
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            raise ValueError(f"Error executing query: {str(e)}")

    def get_table_schemas(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        schemas = []
        for table in tables:
            table_name = table[0]
            columns = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
            schemas.append((table_name, columns))
        return schemas


# Abstract base class for UI operations
class UIInterface(ABC):
    @abstractmethod
    def display_question(self, question, schemas):
        pass

    @abstractmethod
    def get_user_query(self):
        pass

    @abstractmethod
    def display_results(self, user_result, correct_result):
        pass

    @abstractmethod
    def display_error(self, message):
        pass

    @abstractmethod
    def clear_query(self):
        pass

    @abstractmethod
    def try_again(self):
        pass

    @abstractmethod
    def next_question(self):
        pass

    @abstractmethod
    def show_hint(self, hint):
        pass

    @abstractmethod
    def update_progress(self, current_index, total):
        pass

    @abstractmethod
    def display_completion_message(self):
        pass


# ipywidgets UI implementation
class IpywidgetsUI(UIInterface):
    def __init__(self):
        self.quiz = None  # Will be set later
        self.displayed = False  # To prevent multiple displays
        self.setup_ui()

    def set_quiz(self, quiz):
        self.quiz = quiz

    def setup_ui(self):
        self.progress_bar = IntProgress(min=0, max=1, value=0, description='Progress:')
        self.question_label = HTMLWidget(value='')
        
        self.text_area = Textarea(placeholder='Type your SQL query here...', 
                                  layout=Layout(width='100%', height='150px'))
        self.submit_button = Button(description="Submit", button_style='success')
        self.clear_button = Button(description="Clear", button_style='warning')
        self.hint_button = Button(description="Hint", button_style='info')
        
        self.skip_input = IntText(value=1, min=1, layout=Layout(width='60px'))
        self.skip_button = Button(description="Skip to", button_style='info')
        self.skip_box = HBox([Label('Go to question:'), self.skip_input, self.skip_button])

        self.submit_button.on_click(lambda _: self.quiz.submit_query())
        self.clear_button.on_click(lambda _: self.clear_query())
        self.skip_button.on_click(lambda _: self.skip_to_question())
        self.hint_button.on_click(lambda _: self.quiz.show_hint())
    
        self.query_box = VBox([self.text_area, 
                               HBox([self.submit_button, self.clear_button, self.hint_button]),
                               self.skip_box])
        
        self.results_area = HTMLWidget(value='')
        self.try_again_button = Button(description="Try Again", button_style='warning')
        self.next_button = Button(description="Next Question", button_style='info')
        self.try_again_button.on_click(lambda _: self.quiz.try_again())
        self.next_button.on_click(lambda _: self.quiz.next_question())
        
        self.results_box = VBox([self.results_area, HBox([self.try_again_button, self.next_button])])
        
        self.tab = Tab(children=[self.query_box, self.results_box])
        self.tab.set_title(0, 'Query')
        self.tab.set_title(1, 'Results')
        
        self.main_box = VBox([self.progress_bar, self.question_label, self.tab])

    def display_question(self, question, schemas):
        clear_output(wait=True)
        schema_html = self.render_table_schemas(schemas)
        self.question_label.value = (f"<h3>Question {self.quiz.current_index + 1} of {self.quiz.total_questions}:</h3>"
                                     f"<p>{question}</p>{schema_html}")
        self.text_area.value = ''
        self.submit_button.disabled = False
        self.skip_input.max = self.quiz.total_questions
        self.tab.selected_index = 0  # Switch to Query tab
        if not self.displayed:
            display(self.main_box)
            self.displayed = True

    def get_user_query(self):
        return self.text_area.value.strip()

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

    def clear_query(self):
        self.text_area.value = ''

    def try_again(self):
        self.tab.selected_index = 0  # Switch back to Query tab

    def next_question(self):
        self.quiz.next_question()

    def show_hint(self, hint):
        self.results_area.value = f"<h3>Hint:</h3><p>{hint}</p>"
        self.tab.selected_index = 1  # Switch to Results tab

    def update_progress(self, current_index, total):
        self.progress_bar.max = total
        self.progress_bar.value = current_index

    def focus_query_input(self):
        pass  # Not implemented in ipywidgets

    def render_table_schemas(self, schemas):
        schema_html = "<h3>Database Schema:</h3><ul>"
        for table_name, columns in schemas:
            column_info = ", ".join(f"{column[1]} {column[2]}" for column in columns)
            schema_html += f"<li><b>{table_name}</b> ({column_info})</li>"
        schema_html += "</ul>"
        return schema_html

    def skip_to_question(self):
        new_index = self.skip_input.value - 1
        if 0 <= new_index < self.quiz.total_questions:
            self.quiz.current_index = new_index
            self.quiz.display_current_question()
        else:
            self.display_error(f"Invalid question number. Please enter a number between 1 and {self.quiz.total_questions}.")

    def display_completion_message(self):
        self.main_box.children = [HTMLWidget(value="<h2>All questions completed. Well done!</h2>")]
        clear_output(wait=True)
        display(self.main_box)


# Main Quiz class
class Quiz:
    def __init__(self, database: DatabaseInterface, ui: UIInterface, questions, answers):
        self.database = database
        self.ui = ui
        self.questions = questions
        self.answers = answers
        self.current_index = 0
        self.total_questions = len(questions)
        self.ui.set_quiz(self)

    def start(self):
        self.display_current_question()

    def display_current_question(self):
        schemas = self.database.get_table_schemas()
        question = self.questions[self.current_index]
        self.ui.display_question(question, schemas)
        self.ui.update_progress(self.current_index + 1, self.total_questions)

    def submit_query(self):
        user_query = self.ui.get_user_query()
        if not user_query.lower().startswith('select'):
            self.ui.display_error("Please enter a valid SELECT query.")
            return

        try:
            user_result = self.database.execute_query(user_query)
            correct_query = self.answers[self.current_index]
            correct_result = self.database.execute_query(correct_query)
            self.ui.display_results(user_result, correct_result)
        except ValueError as e:
            self.ui.display_error(str(e))

    def next_question(self):
        self.current_index += 1
        if self.current_index < self.total_questions:
            self.display_current_question()
        else:
            self.ui.display_completion_message()

    def try_again(self):
        self.ui.clear_query()
        self.ui.focus_query_input()

    def show_hint(self):
        correct_query = self.answers[self.current_index]
        words = correct_query.split()
        hint = []
        for i, word in enumerate(words):
            if i % 2 == 0:
                hint.append(word)
            else:
                hint.append('_' * len(word))
        hint = ' '.join(hint)
        self.ui.show_hint(hint)


# Functions to load quizzes
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
    elif quiz_id == "music":
        db_url = "https://github.com/brendanpshea/database_sql/raw/main/data/rs_greatest_albums.db"
        json_url = "https://github.com/brendanpshea/database_sql/raw/main/quiz/sql_music_quiz.json"
    else:
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

    database = SQLiteDatabase(db_path)
    ui = IpywidgetsUI()
    quiz = Quiz(database, ui, questions, answers)
    quiz.start()
