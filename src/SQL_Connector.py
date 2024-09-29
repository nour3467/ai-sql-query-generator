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
    """
    conn = None
    try:
        # Establish connection to the database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        print(f"📝 Running SQL Query: {sql_query}")  # Debugging: Log the SQL Query

        cursor.execute(sql_query)

        # Check if it's a SELECT query
        if cursor.description:  # This means it's a SELECT query
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            results = [dict(zip(column_names, row)) for row in rows]

            print(f"✅ Query executed successfully, retrieved {len(results)} rows.")
            return results  # Return the fetched rows
        else:
            # For non-SELECT queries (INSERT, UPDATE, DELETE)
            conn.commit()  # Commit changes to the database
            print("✅ Non-SELECT query executed successfully.")
            return []  # Return empty list for non-SELECT queries

    except Exception as e:
        print(f"❌ Error executing SQL query: {e}")  # Log any error that occurs
        raise  # Re-raise the exception for handling in the calling function

    finally:
        if conn:
            conn.close()
            print("🔒 Database connection closed.")

