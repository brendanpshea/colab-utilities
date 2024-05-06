import random
from IPython.display import display, HTML

def convert_number(number, from_base, to_base):
    if from_base == "decimal" and to_base == "binary":
        return bin(number)[2:]
    elif from_base == "decimal" and to_base == "octal":
        return oct(number)[2:]
    elif from_base == "decimal" and to_base == "hexadecimal":
        return hex(number)[2:]
    elif from_base == "binary" and to_base == "decimal":
        return str(int(number, 2))
    elif from_base == "binary" and to_base == "octal":
        return oct(int(number, 2))[2:]
    elif from_base == "binary" and to_base == "hexadecimal":
        return hex(int(number, 2))[2:]
    elif from_base == "octal" and to_base == "decimal":
        return str(int(number, 8))
    elif from_base == "octal" and to_base == "binary":
        return bin(int(number, 8))[2:]
    elif from_base == "octal" and to_base == "hexadecimal":
        return hex(int(number, 8))[2:]
    elif from_base == "hexadecimal" and to_base == "decimal":
        return str(int(number, 16))
    elif from_base == "hexadecimal" and to_base == "binary":
        return bin(int(number, 16))[2:]
    elif from_base == "hexadecimal" and to_base == "octal":
        return oct(int(number, 16))[2:]

def get_conversion_question():
    number = random.randint(0, 32)
    conversion_types = [("decimal", "binary"), ("decimal", "octal"), ("decimal", "hexadecimal"),
                        ("binary", "decimal"), ("binary", "octal"), ("binary", "hexadecimal"),
                        ("octal", "decimal"), ("octal", "binary"), ("octal", "hexadecimal"),
                        ("hexadecimal", "decimal"), ("hexadecimal", "binary"), ("hexadecimal", "octal")]
    from_base, to_base = random.choice(conversion_types)
    if from_base == "decimal":
        display_number = f"<span style='color: blue;'>{number}</span>"
        correct_answer = convert_number(number, from_base, to_base)
    elif from_base == "binary":
        display_number = f"<span style='color: green;'>{bin(number)[2:]}</span>"
        correct_answer = convert_number(bin(number)[2:], from_base, to_base)
    elif from_base == "octal":
        display_number = f"<span style='color: orange;'>{oct(number)[2:]}</span>"
        correct_answer = convert_number(oct(number)[2:], from_base, to_base)
    elif from_base == "hexadecimal":
        display_number = f"<span style='color: purple;'>{hex(number)[2:]}</span>"
        correct_answer = convert_number(hex(number)[2:], from_base, to_base)
    return display_number, number, from_base, to_base, correct_answer

def get_robot_message(from_base, to_base):
    robots = [
        ("Decimal Bot", "I love working with base 10! Decimal numbers are the most common in everyday life."),
        ("Binary Bot", "Beep boop! I operate in binary, the language of computers. It's all 0s and 1s for me!"),
        ("Octal Bot", "Hello there! I work with octal numbers. They're like decimal, but with a base of 8!"),
        ("Hex Bot", "Greetings! I specialize in hexadecimal, a compact way to represent larger numbers.")
    ]
    robot_name, robot_message = random.choice(robots)
    return f"{robot_name} says: {robot_message} Now, let's convert from {from_base} to {to_base}!"

def number_convert_game():
    score = 0
    html_output = """
    <html>
    <head>
        <title>Number Conversion Game</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: black;
                color: white;
            }
            .correct { color: green; }
            .incorrect { color: red; }
            .robot-message { color: cyan; }
        </style>
    </head>
    <body>
        <h1>Welcome to the Number Conversion Game!</h1>
        <p>Convert the numbers as requested. Type your answers and hit enter. See if you can get 10 right!</p>
    """
    display(HTML(html_output))
    while score < 10:
        display_number, number, from_base, to_base, correct_answer = get_conversion_question()
        robot_message = get_robot_message(from_base, to_base)
        prompt = f"<p class='robot-message'>{robot_message}</p>Convert {display_number} from {from_base} to {to_base}, or type quit to quit: "
        display(HTML(prompt))
        user_answer = input()
        user_answer = user_answer.strip().lower()
        if user_answer == "quit":
            break
        if user_answer == correct_answer.lower():
            html_output = f"<p class='correct'>Correct!</p>"
            score += 1
        else:
            html_output = f"<p class='incorrect'>Incorrect! The correct answer is {correct_answer}.</p>"
        display(HTML(html_output))
    html_output = f"<h2>Congratulations! You got {score} correct answers.</h2></body></html>"
    display(HTML(html_output))
