import random

statements = {
    "Encapsulation": [
        "Misty's class keeps her Pokéballs as non-public data and provides methods for trainers to interact with them.",
        "Sonic's class controls access to his speed value, ensuring it can only be modified through designated methods.",
        "She-Ra's class ensures her sword can only be accessed and used within the confines of her own class.",
        "Robin from Tiny Titans defines his gadget-related operations as internal to his class, hiding the complexity.",
        "Twilight Sparkle's class restricts direct modification of her magic attributes from outside the class.",
        "He-Man's class protects his strength and power data, providing controlled access through specific methods."
    ],
    "Inheritance": [
        "Pikachu and Raichu's classes acquire the properties and behaviors of the ElectricPokemon class.",
        "Tails' class derives from the FlyingAnimal class, enabling him to have all its flying-related functionalities.",
        "Dot Warner's class builds upon the ToonCharacter class, gaining access to its predefined comedic routines.",
        "Starfire from Tiny Titans' class inherits the traits and abilities of the Superhero class.",
        "Rainbow Dash's class extends the Pegasus class, granting her the capabilities to fly and control weather.",
        "Skeletor's class is derived from the Villain class, inheriting its evil schemes and methods."
    ],
    "Polymorphism": [
        "Meowth's class can be treated as a Pokemon or a TalkingAnimal, depending on the context.",
        "The Chaos Emeralds in Sonic's world can take on different forms and properties in each game.",
        "Yakko, Wakko, and Dot's classes can morph into various characters, showcasing different behaviors.",
        "Raven from Tiny Titans can be represented as both a Superhero and a MagicUser.",
        "The ponies in Equestria can have different roles and abilities while still being considered ponies.",
        "He-Man and She-Ra's classes implement a common interface for wielding their respective weapons."
    ],
    
    "Abstraction": [
    "In Pokémon, the characters' personalities and relationships are represented through simplified dialogue and animations, focusing on key traits rather than full backstories.",
    "Sonic's movements and abilities are portrayed using streamlined physics and exaggerated animations, emphasizing gameplay fluidity over strict realism.",
    "The Animaniacs' world is a simplified, satirical version of real-world Hollywood, featuring caricatures of celebrities and the entertainment industry.",
    "The art style in Tiny Titans simplifies the characters' appearances, using minimalistic designs and exaggerated features to convey their personalities.",
    "The world of My Little Pony is a fantasized representation of real-world locations and societies, using magical elements to explore themes and moral lessons.",
    "He-Man's universe presents a clear distinction between good and evil, using archetypal characters and storylines to represent moral concepts.",
]
    
    ,
    "Badness": [
        "Team Rocket's class directly modifies the private attributes of Ash's Pokemon without proper encapsulation.",
        "Dr. Eggman's class has a single massive method that handles all his evil plans, lacking proper organization.",
        "The Animaniacs' props and scenery have tight dependencies on each other, making changes difficult and error-prone.",
        "Gizmo's class from Tiny Titans has duplicated code for his gadget creation methods, leading to inconsistencies.",
        "The villain classes in My Little Pony have a complex web of inheritance, making it hard to understand and maintain.",
        "Skeletor's class uses global variables for his minions, creating potential conflicts and making the code harder to reason about."
    ]
}

def play_game():
    score = 0
    total_questions = 10
    valid_principles = ["encapsulation", "inheritance", "polymorphism", "abstraction", "badness"]

    print("Welcome to the OOP Principles Game!")
    print("For each code description, enter the corresponding OOP principle:")
    print("Encapsulation, Inheritance, Polymorphism, Abstraction, or Badness\n")
    print("Type 'quit' to exit the game.\n")

    for _ in range(total_questions):
        principle = random.choice(list(statements.keys()))
        statement = random.choice(statements[principle])

        while True:
            print("")
            user_answer = input(f"Description: {statement}\nYour answer: ").strip().lower()

            if user_answer == "quit":
                print(f"Game exited early. Your final score: {score}/{total_questions}")
                return
            elif user_answer in valid_principles:
                if user_answer == principle.lower():
                    print("Correct!")
                    score += 1
                    break
                else:
                    print(f"Incorrect. Try again.")
            else:
                print("Invalid answer. Please enter one of the OOP principles: Encapsulation, Inheritance, Polymorphism, Abstraction, or Badness.")

    print()
    print(f"Game over! Your score: {score}/{total_questions}")

play_game()
