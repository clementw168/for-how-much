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


def remove_database(
    host: str = "localhost",
    port: int = 3306,
    user: str = "root",
    password: Optional[str] = None,
    database: str = "for_how_much",
) -> None:
    """
    Remove the database if it exists.

    Args:
        host: MySQL host
        port: MySQL port
        user: MySQL user
        password: MySQL password
        database: Database name to remove
    """
    try:
        # Connect without specifying database
        conn = pymysql.connect(host=host, port=port, user=user, password=password)

        with conn.cursor() as cursor:
            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]

            if database in databases:
                # Drop the database
                cursor.execute(f"DROP DATABASE {database}")
                logger.info(f"Database '{database}' removed successfully")
            else:
                logger.info(f"Database '{database}' does not exist")

        conn.commit()

    except pymysql.Error as e:
        logger.error(f"Error removing database: {e}")
        raise
    finally:
        if "conn" in locals():
            conn.close()


def main():
    """Main function to run the database removal."""
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
        remove_database(**db_config)
    except Exception as e:
        logger.error(f"Failed to remove database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
