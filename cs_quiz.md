CS Quiz Deliverer (cs_quiz.py)
=================

The CS Quiz Deliverer is a Python script that allows you to take computer science quizzes in the form of interactive Jupyter Notebooks. The script fetches a CSV file containing true/false questions from a provided URL, and it presents the questions to the user one by one. The user can answer each question with "True", "False", or "Quit" to exit the quiz.

Features
--------

-   Fetches true/false questions from a CSV file hosted at a given URL
-   Randomizes the order of the questions
-   Presents questions to the user one by one
-   Allows the user to answer with "True", "False", or "Quit"
-   Provides the user's score and the percentage of correct answers at the end of the quiz

Usage
-----

To use the CS Quiz Deliverer, follow these steps:

1. Download the cs_quiz.py file and `import` the cs_quiz function.
2.  Call the `cs_quiz` function with the URL of the CSV file containing the questions:

  ```python
  cs_quiz('https://example.com/questions.csv')`
  ```
  
  Replace `'https://example.com/questions.csv'` with the actual URL of the CSV file.

3.  Answer the questions by entering "True", "False", or "Quit" when prompted.
4.  After answering all the questions or entering "Quit", the script will display your score and the percentage of correct answers.

CSV File Format
---------------

The CSV file containing the questions should follow this format:

```csv
Question 1,True
Question 2,False 
Question 3,True ...
```

Each line in the CSV file should contain a question and its corresponding answer (either "True" or "False), separated by a comma.

Example
-------

Here's an example of how the CS Quiz Deliverer might look when running:

```
Question 1 of 10: What is the purpose of the "import" statement in Python? (True/False/Quit): True
Question 2 of 10: In object-oriented programming, a class is a blueprint for creating objects. (True/False/Quit): True
Question 3 of 10: The == operator is used to test for object identity in Python. (True/False/Quit): False   ...
You answered 10 out of 10 questions. Your score: 8/10 (0.80)
```

Note that the order of the questions and the actual questions themselves may vary depending on the contents of the CSV file.
