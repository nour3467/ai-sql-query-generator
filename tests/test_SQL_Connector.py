"""
Unit tests for the SQL_Connector module.

@module: test_database_handler
@description: Provides unit tests for the generalized CRUD operations and query execution functions
              in the database_handler module.
"""

import pytest
import os
import sqlite3
from src.SQL_Connector import run_sql_query
from src.database_handler import create_table, insert_record

# Path to test database
TEST_DB = os.path.join(os.path.dirname(__file__), "../data/test_sql_connector.db")


# Setup fixture for database
@pytest.fixture(scope="function")
def setup_database():
    """Setup the test database with required tables and sample data."""

    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Create tables using create_table function from database_handler
    create_table(
        TEST_DB,
        "products",
        {"product_id": "INTEGER PRIMARY KEY", "product_name": "TEXT"}
    )

    create_table(
        TEST_DB,
        "sales",
        {"sale_id": "INTEGER PRIMARY KEY", "product_id": "INTEGER", "sale_amount": "INTEGER", "sale_date": "DATE"}
    )

    # Insert sample data using insert_record function from database_handler
    insert_record(TEST_DB, "products", {"product_id": 1, "product_name": "Widget A"})
    insert_record(TEST_DB, "products", {"product_id": 2, "product_name": "Gadget B"})
    insert_record(TEST_DB, "sales", {"sale_id": 1, "product_id": 1, "sale_amount": 50000, "sale_date": "2024-08-28"})
    insert_record(TEST_DB, "sales", {"sale_id": 2, "product_id": 2, "sale_amount": 45000, "sale_date": "2024-08-29"})

    # Database setup complete
    print("✅ Database setup complete with products and sales tables populated.")

    # The yield indicates when tests run after this
    yield

    # Teardown: Remove the test database after tests are done
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
        print(f"🗑️ Test database {TEST_DB} removed after test completion.")


# The actual test function
def test_run_sql_query(setup_database):
    """Test the SQL query execution in SQL Connector."""

    # Define a sample query
    sql_query = """
    SELECT p.product_name, SUM(s.sale_amount) as total_sales
    FROM products p
    JOIN sales s ON p.product_id = s.product_id
    WHERE s.sale_date >= '2024-08-01'
    GROUP BY p.product_id
    ORDER BY total_sales DESC
    LIMIT 5;
    """

    # Execute the query and fetch results
    results = run_sql_query(TEST_DB, sql_query)

    # Assert the results
    assert len(results) == 2, "❌ SQL query did not return the expected number of results."
    assert results[0]["product_name"] == "Widget A", "❌ First product name does not match expected result."
    assert results[0]["total_sales"] == 50000, "❌ First product sales do not match expected result."
    assert results[1]["product_name"] == "Gadget B", "❌ Second product name does not match expected result."
    assert results[1]["total_sales"] == 45000, "❌ Second product sales do not match expected result."

    print("✅ Test passed: SQL query results are correct.")
