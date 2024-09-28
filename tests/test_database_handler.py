"""
Unit tests for the database_handler module.

@module: test_database_handler
@description: Provides unit tests for the generalized CRUD operations and query execution functions
              in the database_handler module.
"""

import pytest
import os
from database_handler import create_table, insert_record, update_record, delete_record, read_records, read_sql_query

# Test database file name
TEST_DB = "data/test_database.db"

def setup_module(module):
    """
    Setup function to create the test environment.
    This is executed before running the tests.
    """
    # Remove the test database if it already exists to ensure a clean slate
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def teardown_module(module):
    """
    Teardown function to clean up after the tests.
    This is executed after all tests have been run.
    """
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_create_table():
    """ Test the creation of a table in the database. """
    create_table(TEST_DB, "EMPLOYEE", {"NAME": "VARCHAR(50)", "AGE": "INT", "DEPARTMENT": "VARCHAR(50)"})
    # Check if the table exists by querying SQLite's master table
    result = read_sql_query(TEST_DB, "SELECT name FROM sqlite_master WHERE type='table' AND name='EMPLOYEE';")
    assert len(result) == 1

def test_insert_record():
    """ Test the insertion of a record into the EMPLOYEE table. """
    insert_record(TEST_DB, "EMPLOYEE", {"NAME": "John Doe", "AGE": 30, "DEPARTMENT": "HR"})
    records = read_records(TEST_DB, "EMPLOYEE")
    assert len(records) == 1
    assert records[0] == ("John Doe", 30, "HR")

def test_update_record():
    """ Test updating a record in the EMPLOYEE table. """
    # Update John's age from 30 to 35
    update_record(TEST_DB, "EMPLOYEE", {"AGE": 35}, {"NAME": "John Doe"})
    records = read_records(TEST_DB, "EMPLOYEE")
    assert records[0][1] == 35  # Check if AGE was updated to 35

def test_delete_record():
    """ Test deleting a record from the EMPLOYEE table. """
    delete_record(TEST_DB, "EMPLOYEE", {"NAME": "John Doe"})
    records = read_records(TEST_DB, "EMPLOYEE")
    assert len(records) == 0  # The record should be deleted

def test_sql_query():
    """ Test reading records using a custom SQL query. """
    # Insert multiple records for testing
    insert_record(TEST_DB, "EMPLOYEE", {"NAME": "Alice", "AGE": 25, "DEPARTMENT": "Finance"})
    insert_record(TEST_DB, "EMPLOYEE", {"NAME": "Bob", "AGE": 40, "DEPARTMENT": "Engineering"})

    # Run a custom query
    result = read_sql_query(TEST_DB, "SELECT NAME FROM EMPLOYEE WHERE AGE > 30;")
    assert len(result) == 1
    assert result[0][0] == "Bob"  # Bob's age is greater than 30
