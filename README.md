
# 🌟 AI SQL Query Generator

Welcome to the **AI SQL Query Generator** project! This tool leverages **Google Gemini Pro** and **Langchain** to generate SQL queries from natural language prompts, interact with databases, and return results in real-time.

## 🚀 Project Overview

The initial version of this project provides a basic framework for generating SQL queries using **Google Gemini Pro** and executing them against an **SQLite** database. As the project evolves, future versions will include more advanced features, such as multi-database support, enhanced query optimization, and custom fine-tuning for specific domains.

## 🛠️ Features (v1.0)

- **Natural Language to SQL**: Converts text input into SQL queries using **Google Gemini Pro** models.
- **SQLite Integration**: Executes the generated SQL queries directly on an **SQLite** database.
- **Modular Codebase**: Designed for scalability and future enhancements.

## 📅 Planned Features (Upcoming Versions)

- **Multi-Database Support**: PostgreSQL, MySQL, etc.
- **Advanced Query Parsing**: Better handling of complex queries and joins.
- **Fine-tuning LLM Models**: Custom fine-tuning based on specific datasets.
- **AI-Powered Query Optimization**: Analyze query performance and suggest optimizations.

---

## 🗂️ Project Structure

```plaintext
ai-sql-query-generator/
│
├── data/                  # Example SQLite databases
│   └── sample.db          # Sample database file for testing
│
├── notebooks/             # Jupyter notebooks for exploratory development
│
├── src/                   # Source code for the project
│   ├── main.py            # Entry point for the application
│   ├── sqlite_helper.py   # Helper functions for database interactions
│   ├── query_processing.py # Handles LLM interaction and query generation
│
├── tests/                 # Unit tests for the project
│   └── test_main.py       # Test cases for the main functionality
│
├── .env                   # Environment variables (API keys, etc.)
├── .gitignore             # Ignored files and folders for Git
├── poetry.lock            # Poetry lock file (exact dependency versions)
├── pyproject.toml         # Poetry dependency and project config file
├── README.md              # This README file
└── LICENSE                # License file (MIT)
```

---

## 🛠️ Installation Guide

### Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.10+**
- **Poetry** (Dependency management tool)
  - Install Poetry:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
- **Google Gemini API access** (to interact with the LLM)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-sql-query-generator.git
cd ai-sql-query-generator
```

### Step 2: Activate the Virtual Environment

Activate your virtual environment if you haven’t already created one. You can skip this step if using Poetry's built-in environment.

```bash
py -3.10 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### Step 3: Install Dependencies with Poetry

Poetry will handle all dependencies (and their exact versions) through the `pyproject.toml` and `poetry.lock` files:

```bash
poetry install
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory to store your API keys and other environment variables. Example:

```plaintext
GEMINI_API_KEY=your-google-gemini-api-key
```

### Step 5: Run the Application

To start the AI-powered SQL generator, run the following:

```bash
poetry run python src/main.py
```

---

## 💻 Usage

1. **Text-to-SQL Query**: Provide a natural language question (e.g., "What is the average age of employees?") and receive a corresponding SQL query.
2. **Execute Query**: The generated SQL query is executed against the connected **SQLite** database, and the results are returned.

---


## 🧪 Running Tests

Unit tests ensure that the main functionalities are working correctly. To run the tests, simply execute:

```bash
poetry run pytest
```

### Running Tests with Print Statements

If you'd like to see the `print` statements in real-time during the test execution (which are usually captured by `pytest`), you can disable output capturing using the `-s` flag. This is especially helpful for debugging and understanding the flow of the tests.

For example, to run a specific test and see the output, use the following command:

```bash
pytest -s tests/test_database_handler.py::test_create_table
```

This will display output such as:

```
🚧 Creating table EMPLOYEE in the test database...
✅ Table 'EMPLOYEE' successfully created.
```


---

## 🧳 Versioning Strategy

### 🔄 Versioning Approach

This project follows **Semantic Versioning** to ensure consistent version control. Here’s how we’ll manage the versions:

- **v1.0.x**: Initial versions focused on basic SQL query generation using Google Gemini Pro.
- **v2.x.x**: Introduction of multi-database support, advanced query generation, and model fine-tuning.
- **v3.x.x**: AI-powered query optimization and domain-specific enhancements.

**How to manage versions**:
- Use **Git tags** to manage releases (e.g., `git tag v1.0.0` and `git push origin v1.0.0`).
- Each new feature or bug fix should be developed in a separate branch, with **pull requests** for review and merging into the main branch.

### 📋 Changelog (for future versions)

We will maintain a changelog to track all updates. Here’s an example:

- **v1.0.0**: Initial release with basic Text-to-SQL functionality and SQLite database support.
- **v1.1.0**: Added unit tests and modularized the code.
- **v2.0.0**: Added PostgreSQL and MySQL support (upcoming).

---

## 🛡️ License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## 🤝 Contributing

We welcome contributions! Here’s how you can get started:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Create a pull request and we’ll review it.

---

## 📞 Contact

If you have any questions, feel free to reach out:

- **Author**: ECH. Noureddine
- **Email**: noureddineechchouky@gmail.com
- **GitHub**: [nour3467](https://github.com/nour3467)

---

### Additional Tips for Project Management and Version Control

- **Git Flow**: Use a branching strategy like Git Flow to manage development and release versions. Have dedicated branches for `develop`, `feature`, and `release` cycles.

  Example:
  ```bash
  git checkout -b feature/advanced-query-generation
  ```

- **Automated Version Bumping**: Use Poetry with [bumpversion](https://pypi.org/project/bumpversion/) or `poetry version <patch|minor|major>` to automatically bump versions.

- **Releases**: Each major version release should include an updated changelog, new tags, and updated documentation (README, examples, etc.).

---

### Summary of Versions

1. **v1.0.x**: Basic functionality with SQLite support and simple query generation.
2. **v2.x.x**: Multi-database support (PostgreSQL, MySQL), fine-tuning models for specific use cases.
3. **v3.x.x**: Full AI-powered query optimization and insights generation (e.g., analytics, recommendations).


