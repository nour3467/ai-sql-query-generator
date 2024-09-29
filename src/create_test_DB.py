import sqlite3


def create_company_db():
    """Creates a company.db SQLite database and populates it with sample data."""
    # Create a new SQLite database (or connect to an existing one)
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()

    # Step 1: Create the necessary tables
    cursor.executescript(
        """
        -- Create Departments table
        CREATE TABLE IF NOT EXISTS Departments (
            dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept_name TEXT NOT NULL,
            location TEXT NOT NULL
        );

        -- Create Employees table
        CREATE TABLE IF NOT EXISTS Employees (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES Departments (dept_id)
        );

        -- Create Projects table
        CREATE TABLE IF NOT EXISTS Projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            budget REAL
        );

        -- Create EmployeeProjects table (Many-to-Many relationship)
        CREATE TABLE IF NOT EXISTS EmployeeProjects (
            emp_id INTEGER,
            project_id INTEGER,
            assigned_date TEXT,
            PRIMARY KEY (emp_id, project_id),
            FOREIGN KEY (emp_id) REFERENCES Employees (emp_id),
            FOREIGN KEY (project_id) REFERENCES Projects (project_id)
        );
    """
    )

    # Step 2: Insert sample data into Departments
    cursor.executemany(
        """
        INSERT INTO Departments (dept_name, location)
        VALUES (?, ?)
    """,
        [
            ("HR", "New York"),
            ("Engineering", "San Francisco"),
            ("Marketing", "Los Angeles"),
        ],
    )

    # Step 3: Insert sample data into Employees
    cursor.executemany(
        """
        INSERT INTO Employees (first_name, last_name, age, department_id)
        VALUES (?, ?, ?, ?)
    """,
        [("John", "Doe", 30, 1), ("Jane", "Smith", 28, 2), ("Robert", "Brown", 35, 3)],
    )

    # Step 4: Insert sample data into Projects
    cursor.executemany(
        """
        INSERT INTO Projects (project_name, budget)
        VALUES (?, ?)
    """,
        [("Project Alpha", 100000.00), ("Project Beta", 150000.00)],
    )

    # Step 5: Insert sample data into EmployeeProjects
    cursor.executemany(
        """
        INSERT INTO EmployeeProjects (emp_id, project_id, assigned_date)
        VALUES (?, ?, ?)
    """,
        [(1, 1, "2023-01-01"), (2, 2, "2023-02-15"), (3, 1, "2023-03-05")],
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("✅ Company database created and populated with sample data.")


# Create the company.db database
create_company_db()
