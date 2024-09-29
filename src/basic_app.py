import streamlit as st

# Title of the app
st.title("Basic Streamlit App")

# Basic text
st.write("Hello, World! This is a basic Streamlit app.")

# Input widget
name = st.text_input("Enter your name:")

# Button to trigger the action
if st.button("Submit"):
    st.write(f"Hello, {name}!")

# Display random data in a chart
import numpy as np
import pandas as pd

data = pd.DataFrame({"A": np.random.rand(10), "B": np.random.rand(10)})

st.line_chart(data)
