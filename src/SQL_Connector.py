"""
Generalized module to handle all database operations like table creation, and CRUD operations (Create, Read, Update, Delete).

@module: SQL_connector
@description: Provides functions to handle all database interactions for any table in an SQLite database.
"""


import os
import sqlite3
from database_handler import create_connection


def run_sql_query(db_name, sql_query):
    """
    Executes a given SQL query on the SQLite database and returns the results.

    :param db_name: str : The path to the SQLite database file.
    :param sql_query: str : The SQL query to execute.
    :return: list[dict] : A list of dictionaries representing the rows.
    """
    conn = None  # Initialize conn to None
    try:
        # Step 1: Use the connection from the database_handler
        conn = create_connection(db_name)
        cursor = conn.cursor()

        print(f"📝 Running SQL Query: {sql_query}")

        # Step 2: Execute the query
        cursor.execute(sql_query)

        # Step 3: Fetch all results
        rows = cursor.fetchall()

        # Step 4: Get column names from the cursor
        column_names = [description[0] for description in cursor.description]

        # Step 5: Convert rows into list of dictionaries
        results = [dict(zip(column_names, row)) for row in rows]

        print(f"✅ Query executed successfully, retrieved {len(results)} rows.")
        return results

    except Exception as e:
        print(f"❌ Error executing SQL query: {e}")
        raise

    finally:
        # Step 6: Ensure the connection is closed properly, only if it was established
        if conn:
            conn.close()
            print("🔒 Database connection closed.")
