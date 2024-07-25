from flask import Flask, request, jsonify
import psycopg2
import logging
from datetime import datetime
from flask_cors import CORS

# Configure logging
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

# Database connection details (consider using environment variables)
DB_HOST = "localhost"
DB_NAME = "taskManager"
DB_USER = "postgres"
DB_PASSWORD = "Brajesh@1627"
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
            port=DB_PORT,
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


# Fetch all test cases
@app.route("/api/testcases", methods=["GET"])
def get_testcases():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 
                id, 
                test_case_name, 
                estimate_time, 
                module, 
                priority, 
                status, 
                to_char(last_updated, 'YYYY-MM-DD HH12:MI AM') as last_updated 
            FROM 
                testcases
        """
        )
        testcases = cur.fetchall()
        cur.close()

        result = []
        for tc in testcases:
            test_case_display_name = f"Test Case ID: {tc[0]} (Last Updated: {tc[6]})"
            result.append(
                {
                    "id": tc[0],
                    "test_case_name": test_case_display_name,
                    "estimate_time": tc[2],
                    "module": tc[3],
                    "priority": tc[4],
                    "status": tc[5],
                    "last_updated": tc[6],
                }
            )

        return jsonify(result)
    except Exception as error:
        logging.error(f"Error fetching test cases: {error}")
        return jsonify({"error": "Failed to fetch test cases"}), 500
    finally:
        close_connection(conn)


# Update test case status
@app.route("/api/testcases/<int:id>", methods=["PUT"])
def update_testcase(id):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database"}), 500

    try:
        status = request.json.get("status")
        now = datetime.now().replace(second=0, microsecond=0)  
        cur = conn.cursor()
        # Update the test case
        cur.execute(
            "UPDATE testcases SET status = %s, last_updated = %s WHERE id = %s",
            (status, now, id),
        )
        conn.commit()

        # Fetch the updated time
        cur.execute(
            "SELECT to_char(last_updated, 'YYYY-MM-DD HH12:MI AM') as last_updated FROM testcases WHERE id = %s",
            (id,)
        )
        updated_last_updated = cur.fetchone()[0]
        cur.close()

        return jsonify({"message": "Test case updated", "last_updated": updated_last_updated})
    except Exception as error:
        logging.error(f"Error updating test case: {error}")
        return jsonify({"error": "Failed to update test case"}), 500
    finally:
        close_connection(conn)


if __name__ == '__main__':
    app.run(debug=True)
