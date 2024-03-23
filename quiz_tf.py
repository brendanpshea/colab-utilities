def load_questions_from_file(file_path):
    questions = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row_num, row in enumerate(reader, start=1):
                if len(row) != 2:
                    print(f"Invalid format in CSV file at line {row_num}: {row}")
                    continue
                question = row[0]
                answer = convert_answer(row[1])
                if answer is None:
                    print(f"Missing or invalid answer in CSV file at line {row_num}: {row}")
                    continue
                questions.append((question, bool(int(answer))))
        return questions
    except Exception as e:
        print(f"An error occurred while loading questions from the file: {str(e)}")
        return []

def load_questions_from_url(url):
    questions = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.text
        reader = csv.reader(csv_data.splitlines())
        for row_num, row in enumerate(reader, start=1):
            if len(row) != 2:
                print(f"Invalid format in CSV data from URL at line {row_num}: {row}")
                continue
            question = row[0]
            answer = convert_answer(row[1])
            if answer is None:
                print(f"Missing or invalid answer in CSV data from URL at line {row_num}: {row}")
                continue
            questions.append((question, bool(int(answer))))
        return questions
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while loading questions from the URL: {str(e)}")
        return []
    except Exception as e:
        print(f"An error occurred while processing the CSV data from the URL: {str(e)}")
        return []
