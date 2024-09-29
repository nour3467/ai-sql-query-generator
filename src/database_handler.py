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
    if not os.path.exists("data"):
        os.makedirs("data")
        print("📂 'data' directory created.")

    # If db_name already has the full path (e.g., "data/test_sql_connector.db"), don't append 'data'
    db_path = (
        db_name
        if os.path.isabs(db_name) or db_name.startswith("data")
        else os.path.join("data", db_name)
    )

    print(f"🔌 Connecting to database: {db_path}")
    return sqlite3.connect(db_path)


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

    db_path = os.path.join('data', db_name)

    print(f"🔌 Connecting to database: {db_path}")
    return sqlite3.connect(db_path)


# --- List Existing Databases ---
def list_databases():
    """
    Lists all the SQLite databases in the 'data' folder.

    @return: list : A list of database filenames in the 'data' directory.
    """
    if not os.path.exists('data'):
        print("📂 'data' directory does not exist, creating it...")
        os.makedirs('data')

    databases = [db for db in os.listdir('data') if db.endswith('.db')]

    if databases:
        print(f"📚 Found {len(databases)} database(s): {databases}")
    else:
        print("❌ No databases found in the 'data' directory.")

    return databases


# --- List Tables in a Database ---
def list_tables(db_name):
    """
    Lists all tables in the specified SQLite database.

    @param db_name: str : The name of the SQLite database file.
    @return: list : A list of table names in the database.
    """
    try:
        conn = create_connection(db_name)
        cursor = conn.cursor()

        print(f"📋 Listing all tables in database: {db_name}")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        conn.close()

        if tables:
            print(f"✅ Found {len(tables)} table(s): {[table[0] for table in tables]}")
            return [table[0] for table in tables]
        else:
            print(f"❌ No tables found in database: {db_name}")
            return []

    except sqlite3.Error as e:
        print(f"❌ Error listing tables in database {db_name}: {e}")
        return []


# --- Create a New Database ---
def create_new_database(db_name):
    """
    Creates a new SQLite database file in the 'data' folder if it doesn't exist.

    @param db_name: str : The name of the new database file.
    @return: None
    """
    db_path = os.path.join('data', db_name)

    if os.path.exists(db_path):
        print(f"⚠️ Database '{db_name}' already exists.")
    else:
        try:
            conn = create_connection(db_name)
            conn.close()
            print(f"✅ New database '{db_name}' created successfully at: {db_path}")
        except sqlite3.Error as e:
            print(f"❌ Error creating database '{db_name}': {e}")


# --- Get Table Structure (Schema) ---
def get_table_structure(db_name, table_name):
    """
    Retrieves the structure (schema) of a specified table in the database.

    @param db_name: str : The name of the SQLite database file.
    @param table_name: str : The name of the table to retrieve the structure for.
    @return: list : A list of tuples representing the columns and their properties.
    """
    try:
        conn = create_connection(db_name)
        cursor = conn.cursor()

        print(f"🔍 Retrieving structure of table '{table_name}' from database: {db_name}")
        cursor.execute(f"PRAGMA table_info({table_name});")
        structure = cursor.fetchall()

        conn.close()

        if structure:
            print(f"✅ Retrieved structure for table '{table_name}': {structure}")
            return structure
        else:
            print(f"❌ No structure found for table '{table_name}' in database '{db_name}'")
            return []

    except sqlite3.Error as e:
        print(f"❌ Error retrieving structure for table '{table_name}' in database '{db_name}': {e}")
        return []


# --- Check if Database Exists ---
def database_exists(db_name):
    """
    Checks if the specified SQLite database exists in the 'data' folder.

    @param db_name: str : The name of the SQLite database file.
    @return: bool : True if the database exists, False otherwise.
    """
    db_path = os.path.join('data', db_name)
    exists = os.path.exists(db_path)

    if exists:
        print(f"✅ Database '{db_name}' exists at: {db_path}")
    else:
        print(f"❌ Database '{db_name}' does not exist.")

    return exists



def get_db_schema(db_name):
    """
    Retrieves the full schema (structure) of all tables in the SQLite database.

    @param db_name: str : The name of the SQLite database file.
    @return: dict : A dictionary where the keys are table names and the values are lists of tuples representing the columns and their properties.
    """
    try:
        conn = create_connection(db_name)
        cursor = conn.cursor()

        # Step 1: Retrieve all table names from the sqlite_master table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print(f"❌ No tables found in database '{db_name}'")
            return {}

        db_schema = {}

        # Step 2: Loop through all tables and get their structure using PRAGMA table_info
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            structure = cursor.fetchall()
            db_schema[table_name] = structure

            print(f"✅ Retrieved structure for table '{table_name}'")

        # Close connection
        conn.close()

        return db_schema

    except sqlite3.Error as e:
        print(f"❌ Error retrieving database schema for '{db_name}': {e}")
        return {}