"""
Generalized module to handle all database operations like table creation, and CRUD operations (Create, Read, Update, Delete).

@module: database_handler
@description: Provides functions to handle all database interactions for any table in an SQLite database.
"""

import os
import sqlite3

# --- Connection Management ---
def create_connection(db_name):
    """
    Creates a connection to the SQLite database.

    @param db_name: str : The path to the SQLite database file.
    @return: sqlite3.Connection : The connection object to the SQLite database.
    """
    # Ensure the 'data' directory exists 📁
    if not os.path.exists('data'):
        os.makedirs('data')
        print("📂 'data' directory created.")

    print(f"🔌 Connecting to database: {db_name}")
    return sqlite3.connect(db_name)


# --- Table Operations ---
def create_table(db_name, table_name, columns):
    """
    Creates a table with the specified columns if it doesn't exist.

    @param db_name: str : The name of the SQLite database file.
    @param table_name: str : The name of the table to be created.
    @param columns: dict : A dictionary with column names as keys and data types as values.
                        Example: {"NAME": "VARCHAR(25)", "AGE": "INT", "CLASS": "VARCHAR(25)"}
    @return: None
    """
    conn = create_connection(db_name)
    cursor = conn.cursor()

    columns_definition = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});"

    print(f"🛠️ Creating table: {table_name} with columns: {columns}")
    cursor.execute(query)

    conn.commit()
    conn.close()
    print(f"✅ Table '{table_name}' created successfully.")


# --- Record Insertion ---
def insert_record(db_name, table_name, data):
    """
    Inserts a record into the specified table.

    @param db_name: str : The name of the SQLite database file.
    @param table_name: str : The name of the table where the record will be inserted.
    @param data: dict : A dictionary where keys are column names and values are the corresponding data.
                      Example: {"NAME": "Alice", "AGE": 23, "CLASS": "Data Science"}
    @return: None
    """
    conn = create_connection(db_name)
    cursor = conn.cursor()

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    values = tuple(data.values())

    print(f"📤 Inserting record into {table_name}: {data}")
    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)

    conn.commit()
    conn.close()
    print(f"✅ Record inserted successfully into {table_name}.")


# --- Record Updating ---
def update_record(db_name, table_name, data, condition):
    """
    Updates a record in the specified table.

    @param db_name: str : The name of the SQLite database file.
    @param table_name: str : The name of the table where the record will be updated.
    @param data: dict : A dictionary where keys are column names to be updated and values are the new data.
                      Example: {"AGE": 24, "CLASS": "AI"}
    @param condition: dict : A dictionary specifying the condition for which record(s) to update.
                            Example: {"NAME": "Alice"}
    @return: None
    """
    conn = create_connection(db_name)
    cursor = conn.cursor()

    set_clause = ', '.join([f"{col} = ?" for col in data])
    condition_clause = ' AND '.join([f"{col} = ?" for col in condition])
    values = tuple(data.values()) + tuple(condition.values())

    print(f"🔄 Updating {table_name} with data: {data} where {condition}")
    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}", values)

    conn.commit()
    conn.close()
    print(f"✅ Record updated in {table_name} where {condition}.")


# --- Record Deletion ---
def delete_record(db_name, table_name, condition):
    """
    Deletes a record from the specified table.

    @param db_name: str : The name of the SQLite database file.
    @param table_name: str : The name of the table from which the record will be deleted.
    @param condition: dict : A dictionary specifying the condition for which record(s) to delete.
                            Example: {"NAME": "Alice"}
    @return: None
    """
    conn = create_connection(db_name)
    cursor = conn.cursor()

    condition_clause = ' AND '.join([f"{col} = ?" for col in condition])
    values = tuple(condition.values())

    print(f"❌ Deleting record from {table_name} where {condition}")
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition_clause}", values)

    conn.commit()
    conn.close()
    print(f"✅ Record deleted from {table_name} where {condition}.")


# --- Read Records ---
def read_records(db_name, table_name):
    """
    Reads all records from the specified table.

    @param db_name: str : The name of the SQLite database file.
    @param table_name: str : The name of the table to read records from.
    @return: list : A list of tuples representing the rows in the specified table.
    """
    conn = create_connection(db_name)
    cursor = conn.cursor()

    print(f"📖 Reading all records from {table_name}")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    conn.close()
    print(f"✅ Retrieved {len(rows)} record(s) from {table_name}.")
    return rows


# --- Execute Custom SQL Query ---
def read_sql_query(db_name, sql_query):
    """
    Executes a given SQL query and returns the result.

    @param db_name: str : The name of the SQLite database file.
    @param sql_query: str : The SQL query to execute.
    @return: list : A list of tuples representing the result of the query.
    """
    conn = create_connection(db_name)
    cursor = conn.cursor()

    print(f"📝 Executing SQL query: {sql_query}")
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    conn.close()
    print(f"✅ Query executed successfully, retrieved {len(rows)} row(s).")
    return rows
