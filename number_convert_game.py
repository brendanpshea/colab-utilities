import random

def convert_number(number, from_base, to_base):
    if from_base == "decimal" and to_base == "binary":
        return bin(number)[2:]
    elif from_base == "decimal" and to_base == "hexadecimal":
        return hex(number)[2:]
    elif from_base == "binary" and to_base == "decimal":
        return int(number, 2)
    elif from_base == "binary" and to_base == "hexadecimal":
        return hex(int(number, 2))[2:]
    elif from_base == "hexadecimal" and to_base == "decimal":
        return int(number, 16)
    elif from_base == "hexadecimal" and to_base == "binary":
        return bin(int(number, 16))[2:]

def get_conversion_question():
    number = random.randint(0, 32)
    conversion_types = [("decimal", "binary"), ("decimal", "hexadecimal"),
                        ("binary", "decimal"), ("binary", "hexadecimal"),
                        ("hexadecimal", "decimal"), ("hexadecimal", "binary")]
    from_base, to_base = random.choice(conversion_types)

    if from_base == "decimal":
        display_number = number
    elif from_base == "binary":
        display_number = bin(number)[2:]
    elif from_base == "hexadecimal":
        display_number = hex(number)[2:]

    correct_answer = convert_number(display_number, from_base, to_base)
    return display_number, from_base, to_base, correct_answer

def number_convert_game():
    score = 0
    print("Welcome to the Number Conversion Game!\n")
    print("Convert the numbers as requested. Type your answers and hit enter. See if you can get 10 right!\n")

    while score < 10:
        number, from_base, to_base, correct_answer = get_conversion_question()
        prompt = f"Convert {number} from {from_base} to {to_base}, or type quit to quit: "
        user_answer = input(prompt).strip().lower()

        if user_answer.lower() == "quit":
          break

        if user_answer == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect! The correct answer is {correct_answer}.")

    print(f"Congratulations! You got {score} correct answers.")
