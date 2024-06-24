def logical_data_models_quiz():
    import random
    statements = {
        "flat": [
            "Data is stored in a single table or file.",
            "No relationships between data entities.",
            "Simple and easy to implement.",
            "Suitable for small datasets.",
            "Examples include CSV files and Excel spreadsheets.",
            "Limited scalability for large datasets.",
            "No support for complex queries.",
            "Data redundancy is common.",
            "Best for simple and quick data storage.",
            "Low performance for complex operations."
        ],
        "relational": [
            "Data is organized into tables with rows and columns.",
            "Tables can be linked by primary and foreign keys.",
            "Supports complex queries using SQL.",
            "Ensures data integrity and reduces redundancy.",
            "Examples include MySQL and PostgreSQL.",
            "Supports ACID transactions.",
            "Normalization to eliminate redundancy.",
            "Easier to maintain and update data.",
            "Best for structured data with clear relationships.",
            "Scalable with indexing and partitioning."
        ],
        "document": [
            "Data is stored in documents, typically JSON or XML.",
            "Each document can have a flexible schema.",
            "Suitable for hierarchical and nested data.",
            "Provides high performance for read and write operations.",
            "Examples include MongoDB and CouchDB.",
            "Supports schema evolution without downtime.",
            "Good for storing unstructured or semi-structured data.",
            "Enables easy horizontal scaling.",
            "Provides rich query capabilities for document-based queries.",
            "Best for content management and catalogs where each item is unique."
        ],
        "graph": [
            "Data is represented as nodes and edges.",
            "Suitable for data with complex relationships.",
            "Enables efficient traversal of data connections.",
            "Used in social networks and recommendation systems.",
            "Examples include Neo4j and ArangoDB.",
            "Supports advanced pathfinding and graph algorithms.",
            "Good for representing highly interconnected data.",
            "Enables real-time recommendations based on relationships.",
            "Best for network analysis and scenarios with many-to-many relationships.",
            "Scalable with graph partitioning to distribute nodes and edges."
        ]
    }

    def play_game():
        score = 0
        total_questions = 10
        valid_models = ["flat", "relational", "document", "graph"]

        print("Welcome to the Star Trek Logical Data Models Quiz!")
        print("For each description, enter the corresponding data model:")
        print("1. Flat, 2. Relational, 3. Document, 4. Graph\n")
        print("Type 'quit' to exit the game.\n")

        for _ in range(total_questions):
            model = random.choice(list(statements.keys()))
            statement = random.choice(statements[model])

            while True:
                print("")
                user_answer = input(f"Statement: {statement}\nYour answer (1-4): ").strip()

                if user_answer == "quit":
                    print(f"Game exited early. Your final score: {score}/{total_questions}")
                    return
                elif user_answer in ["1", "2", "3", "4"]:
                    if user_answer == str(valid_models.index(model) + 1):
                        print("Correct! Engage!")
                        score += 1
                        break
                    else:
                        print("Incorrect. Try again, cadet.")
                else:
                    print("Invalid answer. Please enter 1, 2, 3, or 4.")

            print()

        print(f"Game over! Your score: {score}/{total_questions}")

    play_game()
