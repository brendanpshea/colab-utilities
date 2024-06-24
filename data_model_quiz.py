def logical_data_models_quiz():
    import random
    statements = {
        "flat": [
            "Data is stored in a single table or file, like a CSV.",
            "Best for simple, small datasets with no relationships.",
            "Commonly used in quick-and-dirty data storage solutions.",
            "No support for complex queries; limited to basic operations.",
            "Examples include plain text files and Excel spreadsheets."
        ],
        "relational": [
            "Data is organized into tables with rows and columns.",
            "Tables can be linked using primary and foreign keys.",
            "Ideal for applications requiring complex queries and transactions.",
            "Ensures data integrity with ACID properties.",
            "Common DBMSs include MySQL, PostgreSQL, and Oracle."
        ],
        "document": [
            "Data is stored in documents, typically JSON or BSON.",
            "Flexible schema makes it suitable for unstructured data.",
            "Often used in content management systems and catalogs.",
            "Supports rich queries within documents.",
            "Examples include MongoDB and CouchDB."
        ],
        "graph": [
            "Data is represented as nodes and edges.",
            "Optimal for scenarios with many-to-many relationships, like social networks.",
            "Efficiently handles complex traversals and pathfinding.",
            "Best for applications needing advanced relationship analysis.",
            "Examples include Neo4j and ArangoDB."
        ],
        "wide-column": [
            "Data is stored in columns rather than rows, facilitating fast read operations.",
            "Perfect for analytical queries on large datasets, such as time-series data.",
            "Supports horizontal scaling by adding more columns.",
            "Schema is flexible and can dynamically adapt to new columns.",
            "Examples include Apache Cassandra and HBase."
        ]
    }

    def play_game():
        score = 0
        total_questions = 10
        valid_models = ["flat", "relational", "document", "graph", "wide-column"]

        print("Welcome to the Logical Data Models Quiz!")
        print("For each description, enter the corresponding data model:")
        print("1. Flat, 2. Relational, 3. Document, 4. Graph, 5. Wide-Column\n")
        print("Type 'quit' to exit the game.\n")

        for _ in range(total_questions):
            model = random.choice(list(statements.keys()))
            statement = random.choice(statements[model])

            while True:
                print("")
                user_answer = input(f"Statement: {statement}\nYour answer (1-5): ").strip()

                if user_answer == "quit":
                    print(f"Game exited early. Your final score: {score}/{total_questions}")
                    return
                elif user_answer in ["1", "2", "3", "4", "5"]:
                    if user_answer == str(valid_models.index(model) + 1):
                        print("Correct! Engage!")
                        score += 1
                        break
                    else:
                        print("Incorrect. Try again, cadet.")
                else:
                    print("Invalid answer. Please enter 1, 2, 3, 4, or 5.")

            print()

        print(f"Game over! Your score: {score}/{total_questions}")

    play_game()

logical_data_models_quiz()
