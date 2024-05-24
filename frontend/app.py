import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.title("Custom GPT")

# Initialize chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

# Chat input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        'http://127.0.0.1:8000/chat',
        json={"prompt": prompt}
    ).json()

    if response.get("status") and response.get("data"):
        assistant_response = response["data"]["response"]
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    else:
        st.error("Failed to get response from the server.")
