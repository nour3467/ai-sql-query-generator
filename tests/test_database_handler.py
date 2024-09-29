"""
Unit tests for the database_handler module.

@module: test_database_handler
@description: Provides unit tests for the generalized CRUD operations and query execution functions
              in the database_handler module.
"""

import pytest
import os
import sqlite3
from tqdm import tqdm

from src.database_handler import (
    create_table,
    insert_record,
    update_record,
    delete_record,
    read_records,
    read_sql_query,
    list_databases,
    list_tables,
    create_new_database,
    get_table_structure,
    database_exists,
)

# Define test database names for isolation
TEST_DB = os.path.join(os.path.dirname(__file__), "../data/test_database.db")
NEW_DB = "new_test_database.db"
STRUCTURE_DB = "structure_test_database.db"


def setup_function(function):
    """
    Setup function to prepare specific databases for each test.
    This avoids deleting the whole data folder.
    """
    # Ensure the 'data' directory exists
    os.makedirs("data", exist_ok=True)

    # Clean specific test database files
    for db_name in [TEST_DB, NEW_DB, STRUCTURE_DB]:
        db_path = os.path.join("data", db_name)
        if os.path.exists(db_path):
            os.remove(db_path)


def ensure_table_exists(db_name):
    """Ensures that the EMPLOYEE table exists in the given database."""
    create_table(
        db_name,
        "EMPLOYEE",
        {"NAME": "VARCHAR(50)", "AGE": "INT", "DEPARTMENT": "VARCHAR(50)"},
    )


def test_create_new_database():
    """Test creating a new database."""
    create_new_database(NEW_DB)

    # Verify that the new database exists in the 'data' directory
    assert os.path.exists(
        os.path.join("data", NEW_DB)
    ), "❌ New database creation failed."
    print("✅ New database created successfully.")


def test_database_exists():
    """Test checking if a database exists."""
    # Create a new database for testing
    create_new_database(NEW_DB)

    # Check if the newly created database exists
    assert database_exists(NEW_DB), "❌ Database existence check failed."

    # Check for a non-existing database
    assert not database_exists(
        "non_existing.db"
    ), "❌ Non-existing database incorrectly detected."
    print("✅ Database existence checks passed.")


def test_list_databases():
    """Test listing all existing databases."""
    # Create multiple databases for testing
    create_new_database(NEW_DB)
    create_new_database("another_database.db")

    # List existing databases
    databases = list_databases()

    assert len(databases) == 2, "❌ Incorrect number of databases listed."
    assert NEW_DB in databases, "❌ New test database not found in listing."
    assert (
        "another_database.db" in databases
    ), "❌ Another database not found in listing."
    print("✅ Listing databases successful.")


def test_list_tables():
    """Test listing all tables in the database."""
    ensure_table_exists(TEST_DB)

    # List tables in the database
    tables = list_tables(TEST_DB)

    assert "EMPLOYEE" in tables, "❌ Table 'EMPLOYEE' not found in the database."
    print("✅ Listing tables successful.")


def test_get_table_structure():
    """Test retrieving the structure (schema) of a table."""
    ensure_table_exists(STRUCTURE_DB)  # Use a specific DB for this test

    # Get the structure of the EMPLOYEE table
    structure = get_table_structure(STRUCTURE_DB, "EMPLOYEE")

    assert len(structure) == 3, "❌ Incorrect table structure length."
    assert (
        structure[0][1] == "NAME"
    ), "❌ First column name in table structure mismatch."
    print("✅ Table structure retrieval successful.")


def test_create_table():
    """Test the creation of a table in the database."""
    print("🚧 Creating table EMPLOYEE in the test database...")

    create_table(
        TEST_DB,
        "EMPLOYEE",
        {"NAME": "VARCHAR(50)", "AGE": "INT", "DEPARTMENT": "VARCHAR(50)"},
    )

    # Check if the table exists by querying SQLite's master table
    result = read_sql_query(
        TEST_DB,
        "SELECT name FROM sqlite_master WHERE type='table' AND name='EMPLOYEE';",
    )

    assert len(result) == 1, "❌ Table creation failed."
    print("✅ Table 'EMPLOYEE' successfully created.")


def test_insert_record():
    """Test the insertion of a record into the EMPLOYEE table."""
    print("📤 Inserting record into the EMPLOYEE table...")

    ensure_table_exists(TEST_DB)

    insert_record(
        TEST_DB, "EMPLOYEE", {"NAME": "John Doe", "AGE": 30, "DEPARTMENT": "HR"}
    )

    records = read_records(TEST_DB, "EMPLOYEE")

    assert len(records) == 1, "❌ Record insertion failed."
    assert records[0] == (
        "John Doe",
        30,
        "HR",
    ), "❌ Inserted record does not match expected data."

    print("✅ Record inserted successfully.")


def test_update_record():
    """Test updating a record in the EMPLOYEE table."""
    print("🔄 Updating the AGE field for John Doe...")

    ensure_table_exists(TEST_DB)

    # First, insert a record if it doesn't exist
    insert_record(
        TEST_DB, "EMPLOYEE", {"NAME": "John Doe", "AGE": 30, "DEPARTMENT": "HR"}
    )

    # Update John's age from 30 to 35
    update_record(TEST_DB, "EMPLOYEE", {"AGE": 35}, {"NAME": "John Doe"})

    records = read_records(TEST_DB, "EMPLOYEE")

    assert records[0][1] == 35, "❌ Record update failed (AGE not updated)."

    print("✅ Record updated successfully.")


def test_delete_record():
    """Test deleting a record from the EMPLOYEE table."""
    print("❌ Deleting the record for John Doe...")

    ensure_table_exists(TEST_DB)

    # First, insert a record if it doesn't exist
    insert_record(
        TEST_DB, "EMPLOYEE", {"NAME": "John Doe", "AGE": 30, "DEPARTMENT": "HR"}
    )

    delete_record(TEST_DB, "EMPLOYEE", {"NAME": "John Doe"})

    records = read_records(TEST_DB, "EMPLOYEE")

    assert len(records) == 0, "❌ Record deletion failed."

    print("✅ Record deleted successfully.")


def test_sql_query():
    """Test reading records using a custom SQL query."""
    print("📤 Inserting multiple records for query testing...")

    ensure_table_exists(TEST_DB)

    # Insert multiple records for testing
    with tqdm(
        total=2,
        desc="Inserting records",
        bar_format="{l_bar}{bar} [{elapsed} <{remaining}]",
    ) as pbar:
        insert_record(
            TEST_DB, "EMPLOYEE", {"NAME": "Alice", "AGE": 25, "DEPARTMENT": "Finance"}
        )
        pbar.update(1)

        insert_record(
            TEST_DB, "EMPLOYEE", {"NAME": "Bob", "AGE": 40, "DEPARTMENT": "Engineering"}
        )
        pbar.update(1)

    print("🔍 Running custom SQL query (AGE > 30)...")

    # Run a custom query
    result = read_sql_query(TEST_DB, "SELECT NAME FROM EMPLOYEE WHERE AGE > 30;")

    assert len(result) == 1, "❌ SQL query failed to return the correct result."
    assert (
        result[0][0] == "Bob"
    ), "❌ SQL query did not return the correct record (Bob)."

    print("✅ Custom SQL query executed successfully, Bob's record retrieved.")
