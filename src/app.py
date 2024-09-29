import streamlit as st
import os
import pandas as pd
from database_handler import (
    list_databases,
    create_new_database,
    get_db_schema,
    list_tables,
    insert_record,
    read_records,
    create_table,
)
from SQL_Connector import run_sql_query
from SQL_generator import generate_sql_with_gemini
from Query_prepocessor import preprocess_query_with_gemini

# --- Initialize session state ---
if "selected_db" not in st.session_state:
    st.session_state.selected_db = None
if "generated_query" not in st.session_state:
    st.session_state.generated_query = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --- Sidebar for database management ---
with st.sidebar:
    st.title("📂 Database Management")
    st.info("Start by uploading your SQLite `.db` file", icon="ℹ️")

    # Upload database
    uploaded_file = st.file_uploader("Upload SQLite Database", type=["db"])
    if uploaded_file:
        if not os.path.exists("data"):
            os.makedirs("data")
        with open(f"data/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.selected_db = uploaded_file.name
        st.success(f"✅ Database '{uploaded_file.name}' uploaded successfully.")

    st.markdown("### 💡 Available Commands")

    # Remove visible Copy buttons (just using markdown as hoverable text now)
    st.markdown("#### 🗂 `/list_DBs`")
    st.markdown("#### 📁 `/create_DB <database_name>`")
    st.markdown("#### 🛠 `/select_DB <database_name>`")
    st.markdown("#### 📑 `/list_tables`")
    st.markdown("#### ➕ `/create_table <table_name>`")
    st.markdown("#### ➕ `/insert_into <table_name>`")
    st.markdown("#### 📖 `/read_records <table_name>`")
    st.markdown("#### ✏️ `/update_table <table_name>`")
    st.markdown("#### ❌ `/delete_from <table_name>`")
    st.markdown("#### 💬 **Chat with DB** (Type a natural language query)")


# --- Helper Functions ---
def add_to_chat_history(role, text):
    """Adds a message to the chat history."""
    st.session_state.chat_history.append({"role": role, "text": text})


def display_chat_history():
    """Displays chat history between user and assistant."""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])


# --- Command Handlers ---
def handle_list_dbs():
    """Lists all available databases."""
    with st.spinner("🗂️ Listing databases..."):
        dbs = list_databases()
        if dbs:
            st.write(dbs)
            add_to_chat_history("assistant", f"Available databases: {dbs}")
        else:
            st.warning(
                "⚠️ No databases found. Use `/create_DB <database_name>` to create one."
            )
            add_to_chat_history("assistant", "No databases found.")


def handle_create_db(user_input):
    """Creates a new database."""
    try:
        db_name = user_input.split()[1]
        create_new_database(db_name)
        st.success(f"✅ Database '{db_name}' created successfully.")
        add_to_chat_history("assistant", f"Database '{db_name}' created successfully.")
    except IndexError:
        st.error("⚠️ Please provide a database name after `/create_DB`.")
        add_to_chat_history("assistant", "Error: No database name provided.")


def handle_select_db(user_input):
    """Selects a database (works with or without `.db` extension)."""
    try:
        db_name = user_input.split()[1]
        if not db_name.endswith(".db"):
            db_name += ".db"

        if db_name in list_databases():
            st.session_state.selected_db = db_name
            st.success(f"✅ Database '{db_name}' selected.")
            add_to_chat_history("assistant", f"Database '{db_name}' selected.")
        else:
            st.error(f"❌ Database '{db_name}' not found.")
            add_to_chat_history("assistant", f"Error: Database '{db_name}' not found.")
    except IndexError:
        st.error("⚠️ Please provide a database name after `/select_DB`.")
        add_to_chat_history("assistant", "Error: No database name provided.")


def handle_insert(db_name, table_name, data):
    """
    Inserts records into a table using the insert_record function from database_handler.
    Expects `data` to be a list of column-value pairs or similar.
    """
    try:
        # Convert list data into dictionary form (for column-value pairs)
        # Assuming the data is passed as ['column1=value1', 'column2=value2', ...]
        data_dict = {}
        for item in data:
            key_value = item.split("=")
            if len(key_value) == 2:
                key, value = key_value
                data_dict[key.strip()] = value.strip()

        # Ensure data_dict is passed to the insert function
        insert_record(db_name, table_name, data_dict)
        st.success(f"✅ Record inserted into {table_name}.")
        add_to_chat_history("assistant", f"Record inserted into {table_name}.")
    except Exception as e:
        st.error(f"❌ Error inserting record: {e}")
        add_to_chat_history("assistant", f"Error inserting record: {e}")


def handle_read(db_name, table_name):
    """Reads all records from a table using the read_records function from database_handler."""
    try:
        records = read_records(db_name, table_name)
        df = pd.DataFrame(records)
        st.dataframe(df)
        add_to_chat_history("assistant", f"Records from {table_name}: {records}")
    except Exception as e:
        st.error(f"❌ Error reading records from {table_name}: {e}")
        add_to_chat_history(
            "assistant", f"Error reading records from {table_name}: {e}"
        )


def handle_list_tables():
    """Lists all tables in the currently selected database."""
    if st.session_state.selected_db:
        db_name = st.session_state.selected_db
        tables = list_tables(db_name)
        if tables:
            st.write(tables)
            add_to_chat_history(
                "assistant", f"Tables in database '{db_name}': {tables}"
            )
        else:
            st.warning("⚠️ No tables found in the selected database.")
            add_to_chat_history(
                "assistant", f"No tables found in database '{db_name}'."
            )
    else:
        st.error(
            "⚠️ No database selected. Please select a database first using `/select_DB`."
        )
        add_to_chat_history("assistant", "Error: No database selected.")


# --- Natural Language Query to SQL ---
def handle_nl_query(user_input):
    """Processes a natural language query into SQL and executes it."""
    if st.session_state.selected_db:
        with st.spinner("Processing your query..."):
            # Preprocess query with feedback during processing
            preprocessed_query = preprocess_query_with_gemini(user_input)

            # Handle errors during processing
            if "error" in preprocessed_query:
                add_to_chat_history("assistant", f"❌ {preprocessed_query['error']}")
                return

            db_schema = get_db_schema(st.session_state.selected_db)

            # Generate SQL using Google Gemini (or similar tool)
            generated_sql = generate_sql_with_gemini(preprocessed_query, db_schema)
            if generated_sql:
                st.session_state.generated_query = generated_sql
                add_to_chat_history(
                    "assistant", f"Generated SQL:\n```sql\n{generated_sql}\n```"
                )

                # Display and execute the query
                display_query_controls()
            else:
                st.error("❌ Failed to generate SQL query.")
    else:
        st.error("⚠️ Please select a database first.")


# --- Query Controls and Execution ---
def display_query_controls():
    """Displays the generated query with options to modify or validate."""
    if st.session_state.generated_query:
        st.subheader("Generated SQL Query:")
        st.code(st.session_state.generated_query)

        modify_query = st.text_area(
            "Modify the query if needed:", st.session_state.generated_query
        )
        if st.button("Validate & Execute Query"):
            st.session_state.generated_query = modify_query
            execute_query()


def execute_query():
    """Executes the SQL query and displays the results."""
    db_name = st.session_state.selected_db
    query = st.session_state.generated_query

    if query and db_name:
        st.write(f"Executing query on database: {db_name}")  # Debugging step

        try:
            # Call the function to run the SQL query
            results = run_sql_query(db_name, query)
            st.write(f"Query results: {results}")  # Debugging step

            # If results were returned, handle them (for SELECT queries)
            if results:
                df = pd.DataFrame(results)
                if not df.empty:
                    st.dataframe(df)

                    # Provide option to download results as Excel
                    excel_data = df.to_excel(index=False, engine="openpyxl")
                    st.download_button(
                        label="📥 Export Results to Excel",
                        data=excel_data,
                        file_name="query_results.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                else:
                    st.info("ℹ️ Query executed successfully, but no data was returned.")
            else:
                st.info("ℹ️ Query executed successfully. No data to display (likely a non-SELECT query).")
        except Exception as e:
            st.error(f"⚠️ Error executing query: {e}")
            st.write(f"⚠️ Error details: {e}")
    else:
        st.error("⚠️ No query generated or database selected.")





# --- Main App Interface ---
st.title("🔎 SQL Query Generator Studio")
st.markdown(
    "Explore and manage your SQLite databases with ease! 💬 Type commands or natural language queries to interact."
)

# Display chat history
display_chat_history()

# User input handling
user_input = st.chat_input("Type a command or a natural language query...")

if user_input:
    # Display user input in chat history
    with st.chat_message("user"):
        st.markdown(user_input)
    add_to_chat_history("user", user_input)

    # Command Routing
    if user_input.startswith("/list_DBs"):
        handle_list_dbs()
    elif user_input.startswith("/create_DB"):
        handle_create_db(user_input)
    elif user_input.startswith("/select_DB"):
        handle_select_db(user_input)
    elif user_input.startswith("/list_tables"):
        handle_list_tables()
    elif user_input.startswith("/insert_into"):
        # handle insert using `handle_insert`
        # assuming syntax: /insert_into <table_name> [data]
        try:
            parts = user_input.split()
            table_name = parts[1]
            data = parts[2:]
            handle_insert(st.session_state.selected_db, table_name, data)
        except IndexError:
            st.error("⚠️ Invalid insert command.")
    elif user_input.startswith("/read_records"):
        # handle read using `handle_read`
        # assuming syntax: /read_records <table_name>
        try:
            parts = user_input.split()
            table_name = parts[1]
            handle_read(st.session_state.selected_db, table_name)
        except IndexError:
            st.error("⚠️ Invalid read command.")
    else:
        # Process Natural Language Queries
        handle_nl_query(user_input)

# --- Footer ---
st.markdown("---")
st.markdown("👨‍💻 Crafted with ❤️ | 🚀 Powered by Streamlit and Google Gemini Pro.")
