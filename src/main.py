from database_handler import create_new_database

def main():
    """
    Main function to create a new SQLite database by directly calling the function.
    """
    # Specify the database name directly here
    db_name = "test_sql_connector.db"

    # Call the function to create a new database
    create_new_database(db_name)



if __name__ == "__main__":
    main()
