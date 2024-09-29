import os
import google.generativeai as genai
import json
from dotenv import load_dotenv
import spacy

# Load environment variables (such as the Google Gemini API key)
load_dotenv()

# Configure the Gemini Pro API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load spaCy model for NLP tasks
nlp = spacy.load("en_core_web_sm")

def preprocess_query_with_gemini(nl_query):
    """
    Preprocesses the user's natural language query using advanced NLP techniques and Gemini Pro.

    Returns a structured response with the intent, entities, conditions, aggregations, time range, and limit.
    """
    # Initial parsing with spaCy to identify entities and key tokens
    doc = nlp(nl_query)
    entities = [ent.text for ent in doc.ents]

    # Prepare prompt for Gemini Pro with examples
    prompt = f"""
    You are an expert in transforming natural language into SQL components.
    Given a user query, extract the following information in JSON format without any extra text:

    {{
        "intent": <intent such as 'select', 'insert', 'update', 'delete'>,
        "entities": [<list of table names or entities mentioned in the query>],
        "conditions": [<list of conditions such as filters or where clauses>],
        "aggregations": [<list of aggregation functions and fields>],
        "time_range": <time range if specified>,
        "limit": <limit if specified>
    }}

    Example User Query: "Show all employees over the age of 30."
    User Query: "{nl_query}"
    """

    try:
        # Create a generative model instance
        model = genai.GenerativeModel("gemini-pro")

        # Send the prompt to Gemini Pro
        response = model.generate_content([prompt])

        # Extract the structured output from Gemini's response
        structured_output = response.text.strip()
        print(f"⚙️ Gemini Pro response: {structured_output}")  # Debugging

        # Parse the response safely as JSON
        try:
            preprocessed_query = json.loads(structured_output)

            # Basic validation to ensure the 'entities' field is not numeric
            if any(entity.isnumeric() for entity in preprocessed_query.get("entities", [])):
                raise ValueError("Invalid entity detected (numeric value in entities).")

            return preprocessed_query
        except json.JSONDecodeError:
            print(f"❌ Gemini Pro returned an unstructured response. Raw output: {structured_output}")
            return {"error": "Unstructured response from Gemini Pro. Please try again."}
        except ValueError as ve:
            print(f"❌ Validation error: {ve}")
            return {"error": f"Invalid entity in response: {ve}"}

    except Exception as e:
        print(f"❌ Error during query preprocessing with Gemini Pro: {e}")
        return {"error": str(e)}
