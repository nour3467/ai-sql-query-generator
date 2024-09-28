"""
Unit tests for the database_handler module.

@module: test_database_handler
@description: Provides unit tests for the generalized CRUD operations and query execution functions
              in the database_handler module.
"""

import pytest
import os
import sys
from tqdm import tqdm

# Add the parent directory to the system path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database_handler import (
    create_table,
    insert_record,
    update_record,
    delete_record,
    read_records,
    read_sql_query,
)

# Test database file name (using absolute path for better control)
TEST_DB = os.path.join(os.path.dirname(__file__), "../data/test_database.db")


def setup_module(module):
    """
    Setup function to create the test environment.
    This is executed before running the tests.
    """
    print(f"🛠️ Setting up the test environment. Database path: {TEST_DB}")

    # Create the 'data' directory if it doesn't exist
    data_dir = os.path.dirname(TEST_DB)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"📂 Created 'data' directory at: {data_dir}")
    else:
        print(f"📂 'data' directory already exists: {data_dir}")

    # Remove the test database if it already exists to ensure a clean slate
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
        print(f"🗑️ Deleted existing test database: {TEST_DB}")
    else:
        print(f"🆕 No existing test database found, proceeding with fresh start.")


def teardown_module(module):
    """
    Teardown function to clean up after the tests.
    This is executed after all tests have been run.
    """
    print("🧹 Cleaning up the test environment...")

    # Remove the test database after all tests have run
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
        print(f"🗑️ Deleted test database: {TEST_DB}")
    else:
        print(f"✅ No test database found for cleanup.")


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

    # Update John's age from 30 to 35
    update_record(TEST_DB, "EMPLOYEE", {"AGE": 35}, {"NAME": "John Doe"})

    records = read_records(TEST_DB, "EMPLOYEE")

    assert records[0][1] == 35, "❌ Record update failed (AGE not updated)."

    print("✅ Record updated successfully.")


def test_delete_record():
    """Test deleting a record from the EMPLOYEE table."""
    print("❌ Deleting the record for John Doe...")

    delete_record(TEST_DB, "EMPLOYEE", {"NAME": "John Doe"})

    records = read_records(TEST_DB, "EMPLOYEE")

    assert len(records) == 0, "❌ Record deletion failed."

    print("✅ Record deleted successfully.")


def test_sql_query():
    """Test reading records using a custom SQL query."""
    print("📤 Inserting multiple records for query testing...")

    # Using tqdm for progress tracking during record insertion
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
