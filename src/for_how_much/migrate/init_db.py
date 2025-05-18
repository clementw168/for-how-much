import logging
import os
import sys
from typing import Optional

import pymysql
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def create_database(
    host: str = "localhost",
    port: int = 3306,
    user: str = "root",
    password: Optional[str] = None,
    database: str = "for_how_much",
) -> None:
    """
    Create the database if it doesn't exist.

    Args:
        host: MySQL host
        port: MySQL port
        user: MySQL user
        password: MySQL password
        database: Database name to create
    """
    try:
        # First connect without database to create it
        conn = pymysql.connect(host=host, port=port, user=user, password=password)

        with conn.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            logger.info(f"Database '{database}' created or already exists")

            # Use the database
            cursor.execute(f"USE {database}")

            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    questions_seen INT DEFAULT 0,
                    answered_questions JSON
                )
            """)
            logger.info("Table 'users' created or already exists")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text TEXT NOT NULL,
                    image_url VARCHAR(255),
                    type VARCHAR(50) NOT NULL,
                    min_value INT,
                    max_value INT,
                    price_unit VARCHAR(10) NOT NULL,
                    category VARCHAR(50) NOT NULL
                )
            """)
            logger.info("Table 'questions' created or already exists")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stats (
                    question_id INT PRIMARY KEY,
                    average_answer FLOAT NOT NULL,
                    number_of_answers INT NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                )
            """)
            logger.info("Table 'stats' created or already exists")

        conn.commit()
        logger.info("Database setup completed successfully")

    except pymysql.Error as e:
        logger.error(f"Error setting up database: {e}")
        raise
    finally:
        if "conn" in locals():
            conn.close()


def main():
    """Main function to run the database initialization."""
    # Load environment variables
    load_dotenv()

    # Get database configuration from environment variables
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME", "for_how_much"),
    }

    try:
        create_database(**db_config)
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
