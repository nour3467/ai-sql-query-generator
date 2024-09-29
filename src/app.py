import streamlit as st
from database_handler import (
    list_databases, create_new_database, get_db_schema, list_tables, insert_record,
    update_record, delete_record, read_sql_query, read_records, database_exists, get_table_structure, create_table
)

# --- Initialize selected database in session state ---
if "selected_db" not in st.session_state:
    st.session_state.selected_db = None

# --- Initialize chat history ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Helper function to display chat history ---
def display_chat_history():
    """Displays chat history between user and assistant."""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

# --- Helper function to add messages to chat history ---
def add_to_chat_history(role, text):
    """Adds a message to the chat history."""
    st.session_state.chat_history.append({"role": role, "text": text})

# --- Helper function to display database selection notification ---
def notify_selected_db():
    """Displays a notification for the currently selected database."""
    if st.session_state.selected_db:
        st.info(f"🗄️ Currently selected database: `{st.session_state.selected_db}`")
    else:
        st.error("⚠️ Please select a database using `/select_DB <database_name>` before proceeding.")

# --- Command Handlers ---
def handle_list_dbs():
    """Lists all available databases."""
    with st.spinner('🗂️ Listing databases...'):
        st.subheader("🗂️ Available Databases")
        dbs = list_databases()
        if dbs:
            st.write(dbs)
        else:
            st.warning("⚠️ No databases found. Use `/create_DB <database_name>` to create one.")
        add_to_chat_history("assistant", "Processed command: list_DBs")

def handle_create_db(user_input):
    """Handles the creation of a new database."""
    with st.spinner('⚙️ Creating database...'):
        try:
            db_name = user_input.split()[1]
            create_new_database(db_name)
            st.success(f"✅ Database '{db_name}' created successfully.")
            add_to_chat_history("assistant", f"Database '{db_name}' created successfully.")
        except IndexError:
            st.error("⚠️ Please provide a database name after `/create_DB`.")
            add_to_chat_history("assistant", "Error: No database name provided.")

def handle_select_db(user_input):
    """Handles the selection of a database."""
    with st.spinner('🔍 Selecting database...'):
        try:
            db_name = user_input.split()[1]
            if db_name in list_databases():
                st.session_state.selected_db = db_name  # Store the selected database in session state
                st.success(f"✅ Database '{db_name}' selected.")
                add_to_chat_history("assistant", f"Database '{db_name}' selected.")
            else:
                st.error(f"❌ Database '{db_name}' not found.")
                add_to_chat_history("assistant", f"Error: Database '{db_name}' not found.")
        except IndexError:
            st.error("⚠️ Please provide a database name after `/select_DB`.")
            add_to_chat_history("assistant", "Error: No database name provided.")

def handle_list_tables():
    """Lists all tables in the currently selected database."""
    with st.spinner('📋 Listing tables...'):
        if st.session_state.selected_db:
            db_name = st.session_state.selected_db
            tables = list_tables(db_name)
            if tables:
                st.write(tables)
                add_to_chat_history("assistant", f"Tables in database '{db_name}': {tables}")
            else:
                st.warning("⚠️ No tables found in the selected database.")
                add_to_chat_history("assistant", f"No tables found in database '{db_name}'.")
        else:
            st.error("⚠️ No database selected. Please select a database first using `/select_DB`.")
            add_to_chat_history("assistant", "Error: No database selected.")

def handle_create_table(user_input):
    """Handles the creation of a table in the selected database."""
    if st.session_state.selected_db:
        db_name = st.session_state.selected_db
        try:
            table_name = user_input.split()[1]
            columns = st.text_area("Enter columns in the format: column_name data_type (e.g., 'name TEXT, age INTEGER')")
            columns_dict = dict([tuple(col.strip().split()) for col in columns.split(",")])
            if st.button("Create Table"):
                create_table(db_name, table_name, columns_dict)
                st.success(f"✅ Table '{table_name}' created successfully.")
                add_to_chat_history("assistant", f"Table '{table_name}' created successfully in database '{db_name}'.")
        except IndexError:
            st.error("⚠️ Please provide a table name after `/create_table`.")
            add_to_chat_history("assistant", "Error: No table name provided.")
    else:
        st.error("⚠️ No database selected. Please select a database first using `/select_DB`.")
        add_to_chat_history("assistant", "Error: No database selected.")

def handle_insert_into(user_input):
    """Handles insertion of records into a table."""
    if st.session_state.selected_db:
        db_name = st.session_state.selected_db
        try:
            table_name = user_input.split()[1]
            st.subheader(f"➕ Insert into `{table_name}`")
            columns = st.text_area("Enter columns (comma-separated)")
            values = st.text_area("Enter values (comma-separated)")
            if st.button("Insert Record"):
                data = dict(zip(columns.split(","), values.split(",")))
                insert_record(db_name, table_name, data)
                st.success(f"✅ Record inserted into `{table_name}`.")
                add_to_chat_history("assistant", f"Record inserted into table '{table_name}' in database '{db_name}'.")
        except IndexError:
            st.error("⚠️ Please specify the table name after `/insert_into`.")
            add_to_chat_history("assistant", "Error: No table name provided.")
    else:
        st.error("⚠️ No database selected. Please select a database first using `/select_DB`.")
        add_to_chat_history("assistant", "Error: No database selected.")

def handle_read_records(user_input):
    """Handles reading records from a table."""
    if st.session_state.selected_db:
        db_name = st.session_state.selected_db
        try:
            table_name = user_input.split()[1]
            with st.spinner('📖 Reading records...'):
                st.subheader(f"Records in `{table_name}`")
                records = read_records(db_name, table_name)
                st.dataframe(records)
                add_to_chat_history("assistant", f"Read records from table '{table_name}' in database '{db_name}'.")
        except IndexError:
            st.error("⚠️ Please specify the table name after `/read_records`.")
            add_to_chat_history("assistant", "Error: No table name provided.")
    else:
        st.error("⚠️ No database selected. Please select a database first using `/select_DB`.")
        add_to_chat_history("assistant", "Error: No database selected.")

def handle_update_table(user_input):
    """Handles updating records in a table."""
    if st.session_state.selected_db:
        db_name = st.session_state.selected_db
        try:
            table_name = user_input.split()[1]
            st.subheader(f"✏️ Update `{table_name}`")
            condition = st.text_area("Enter condition (e.g., 'name = Alice')")
            update_data = st.text_area("Enter update data (e.g., 'age = 25')")
            if st.button("Update Record"):
                condition_dict = dict([tuple(cond.split("=")) for cond in condition.split(",")])
                update_dict = dict([tuple(update.split("=")) for update in update_data.split(",")])
                update_record(db_name, table_name, update_dict, condition_dict)
                st.success(f"✅ Record updated in `{table_name}`.")
                add_to_chat_history("assistant", f"Record updated in table '{table_name}' in database '{db_name}'.")
        except IndexError:
            st.error("⚠️ Please specify the table name after `/update_table`.")
            add_to_chat_history("assistant", "Error: No table name provided.")
    else:
        st.error("⚠️ No database selected. Please select a database first using `/select_DB`.")
        add_to_chat_history("assistant", "Error: No database selected.")

def handle_delete_from(user_input):
    """Handles deletion of records from a table."""
    if st.session_state.selected_db:
        db_name = st.session_state.selected_db
        try:
            table_name = user_input.split()[1]
            st.subheader(f"❌ Delete from `{table_name}`")
            condition = st.text_area("Enter condition for deletion (e.g., 'name = Alice')")
            if st.button("Delete Record"):
                condition_dict = dict([tuple(cond.split("=")) for cond in condition.split(",")])
                delete_record(db_name, table_name, condition_dict)
                st.success(f"✅ Record deleted from `{table_name}`.")
                add_to_chat_history("assistant", f"Record deleted from table '{table_name}' in database '{db_name}'.")
        except IndexError:
            st.error("⚠️ Please specify the table name after `/delete_from`.")
            add_to_chat_history("assistant", "Error: No table name provided.")
    else:
        st.error("⚠️ No database selected. Please select a database first using `/select_DB`.")
        add_to_chat_history("assistant", "Error: No database selected.")

# --- Main App Header and Description ---
st.title("🔎 SQL Query Generator")
st.markdown("""
    Welcome to the SQL Query Generator! You can interact with databases using natural language queries or commands. 💬

    **Commands**:
    - 🗂 `/list_DBs`: List all available databases.
    - 📁 `/create_DB <database_name>`: Create a new database.
    - 🛠 `/select_DB <database_name>`: Select a database to work with.
    - 📑 `/list_tables`: List tables in the currently selected database.
    - ➕ `/create_table <table_name>`: Create a table in the selected database.
    - ➕ `/insert_into <table_name>`: Insert records into a table.
    - 📖 `/read_records <table_name>`: Read all records from a table.
    - ✏️ `/update_table <table_name>`: Update records in a table.
    - ❌ `/delete_from <table_name>`: Delete records from a table.
""")

# --- Display Chat History ---
display_chat_history()

# --- User Input ---
user_input = st.chat_input("💬 Type a command or query...")

# --- Command Execution ---
if user_input:
    # Display and store user message
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

    elif user_input.startswith("/create_table"):
        handle_create_table(user_input)

    elif user_input.startswith("/insert_into"):
        handle_insert_into(user_input)

    elif user_input.startswith("/read_records"):
        handle_read_records(user_input)

    elif user_input.startswith("/update_table"):
        handle_update_table(user_input)

    elif user_input.startswith("/delete_from"):
        handle_delete_from(user_input)

    # Add system response to chat history
    add_to_chat_history("assistant", "Processed command or query.")

# --- Footer ---
st.markdown("---")
st.markdown("👨‍💻 Crafted with ❤️ | 🚀 Powered by LangChain, Gemini, and Streamlit.")
