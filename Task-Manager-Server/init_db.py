import psycopg2
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Database connection details (consider using environment variables)
DB_HOST = 'localhost'
DB_NAME = 'taskManager'
DB_USER = 'postgres'
DB_PASSWORD = 'Brajesh@1627'
DB_PORT = 5433


def get_connection():
    """
    Function to establish a connection to the database.
    Returns a psycopg2 connection object.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        logging.debug("Connection established successfully")
        return conn
    except Exception as error:
        logging.error(f"Error connecting to database: {error}")
        return None


def close_connection(conn):
    """
    Function to close the database connection.
    Takes a psycopg2 connection object as input.
    """
    if conn:
        conn.close()
        logging.debug("Connection closed successfully")


def initialize_database():
    """
    Function to initialize the database using the init_db.sql script.
    """
    conn = get_connection()
    if not conn:
        return

    try:
        cur = conn.cursor()
        with open('init_db.sql', 'r') as file:
            sql_commands = file.read().split(';')  # Split the commands by semicolon
            for command in sql_commands:
                if command.strip():  # Ignore empty commands
                    cur.execute(command)
        conn.commit()
        cur.close()
        logging.debug("Database initialized successfully")
    except Exception as error:
        logging.error(f"Error initializing database: {error}")
    finally:
        close_connection(conn)


if __name__ == '__main__':
    initialize_database()
