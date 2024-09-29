"""
Generalized module to handle query preprocessing using Google Gemini Pro for complex natural language input.

@module: query_preprocessor
@description: Sends a complex natural language query to Gemini Pro and retrieves structured data for SQL generation.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (such as Google Gemini API key)
load_dotenv()

# Configure the Gemini Pro API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def preprocess_query_with_gemini(nl_query):
    """
    Sends the user's complex natural language query to Google Gemini Pro for preprocessing.

    @param nl_query: str : The user's complex natural language query.
    @return: dict : A structured response with the intent, entities, time range, and other necessary components.
    """
    # Define a clear prompt for Gemini to understand the user's query
    prompt = [
        """
        You are an expert in natural language understanding. You will receive a user query in complex natural language,
        and your job is to extract the following information: intent (such as 'retrieve' or 'aggregate'),
        entities (like 'products' or 'sales'), time range (e.g., 'last month', 'this year'), and limit (e.g., 'top 5').

        Here's an example:
        Input: "Show top 5 products by sales last month"
        Output: {
            "cleaned_query": "show top 5 products by sales last month",
            "entities": ["products", "sales"],
            "time_range": "last month",
            "intent": "aggregate",
            "limit": 5
        }

        Now process the following query:
        """
    ]

    try:
        # Send the user query to Gemini Pro
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], nl_query])

        # Extract the structured output from Gemini's response
        structured_output = response.text.strip()

        # Return structured output from Gemini (assume it is in JSON format)
        return eval(structured_output)

    except Exception as e:
        print(f"❌ Error during query preprocessing with Gemini Pro: {e}")
        return {}

