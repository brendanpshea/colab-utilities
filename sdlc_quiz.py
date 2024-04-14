def sdlc_quiz():
  import random
  statements = {
    "Planning": [
        "Defining the scope and objectives of the project.",
        "Identifying the target audience and their needs.",
        "Estimating the project timeline and resources required.",
        "Conducting feasibility analysis and risk assessment.",
        "Defining the high-level requirements of the software."
    ],
    "Analysis": [
        "Gathering and documenting detailed user requirements.",
        "Creating user stories and use case diagrams.",
        "Analyzing the system's functional and non-functional requirements.",
        "Identifying the system's constraints and assumptions.",
        "Creating data flow diagrams and entity-relationship diagrams."
    ],
    "Design": [
        "Creating the system architecture and design documents.",
        "Designing the user interface and user experience.",
        "Defining the database schema and data models.",
        "Creating class diagrams and sequence diagrams.",
        "Selecting the appropriate technology stack and frameworks."
    ],
    "Implementation": [
        "Writing the source code based on the design specifications.",
        "Implementing the user interface and database components.",
        "Integrating different modules and components of the system.",
        "Conducting unit testing and debugging.",
        "Following coding standards and best practices."
    ],
    "Testing": [
        "Preparing test plans and test cases.",
        "Conducting integration testing and system testing.",
        "Performing user acceptance testing (UAT) with end-users.",
        "Identifying and reporting bugs and issues.",
        "Verifying and validating the system against requirements."
    ],
    "Maintenance": [
        "Monitoring the system's performance and reliability.",
        "Providing ongoing support and troubleshooting.",
        "Implementing bug fixes and system enhancements.",
        "Managing user feedback and incorporating changes.",
        "Performing system updates and upgrades."
    ]
}
  
  def play_game():
      score = 0
      total_questions = 10
      valid_layers = ["planning", "analysis", "design", "implementation", "testing", "maintenance"]

      print("Welcome to the Software Development Lifecycle Quiz!")
      print("For each activity, enter the corresponding stage:")
      print("Planning, Analysis, Design, Implementation, Testing, or Maintenance\n")
      print("Type 'quit' to exit the game.\n")

      for _ in range(total_questions):
          layer = random.choice(list(statements.keys()))
          statement = random.choice(statements[layer])

          while True:
              print("")
              user_answer = input(f"Statement: {statement}\nYour answer: ").strip().lower()

              if user_answer == "quit":
                  print(f"Game exited early. Your final score: {score}/{total_questions}")
                  return
              elif user_answer in valid_layers:
                  if user_answer == layer.lower():
                      print("Correct!")
                      score += 1
                      break
                  else:
                      print(f"Incorrect. Try again.")
              else:
                  print("Invalid answer. Please enter one of the on the stages of the SDLC: Planning, Analysis, Design, Implementation, Testing, Maintenance.")

          print()

      print(f"Game over! Your score: {score}/{total_questions}")

  play_game()
