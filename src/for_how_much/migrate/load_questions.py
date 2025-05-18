import csv

from for_how_much.database import SessionLocal
from for_how_much.models import Question, Stats


def load_questions():
    db = SessionLocal()
    try:
        # Read the CSV file
        with open("data/data_source.csv", "r") as file:
            csv_reader = csv.DictReader(file)

            # Process each row
            for row in csv_reader:
                # Create question
                question = Question(
                    id=int(row["id"]),
                    text=row["text"],
                    image_url=row["image_url"] if row["image_url"] else None,
                    type="slider",  # Default type as per model
                    min_value=int(row["min_value"]) if row["min_value"] else None,
                    max_value=int(row["max_value"]) if row["max_value"] else None,
                    price_unit="$",  # Default unit as per model
                    category=row["category"],
                )

                # Create associated stats
                stats = Stats(
                    question_id=int(row["id"]), average_answer=0.0, number_of_answers=0
                )

                # Add to session
                db.add(question)
                db.add(stats)

            # Commit all changes
            db.commit()
            print("Successfully loaded questions into database!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    load_questions()
