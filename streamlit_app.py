import streamlit as st
import requests

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Hugging Face's model to generate responses. "
    "To use this app, you need to provide a Hugging Face API key once."
)

# Ask user for their Hugging Face API key if it's not already stored.
if "hf_api_key" not in st.session_state:
    hf_api_key = st.text_input("Hugging Face API Key", type="password")
    if hf_api_key:
        # Store the API key in session state and reload to hide the input field.
        st.session_state.hf_api_key = hf_api_key
        # st.experimental_rerun()

# Proceed with the chat interface only if the API key is available in session state.
if "hf_api_key" in st.session_state:
    # Initialize chat messages in session state if not already present.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the chat messages stored in session state.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for the user.
    if prompt := st.chat_input("Ask a question based on the context"):
        # Add user's message to chat history and display it.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Set up Hugging Face API request.
        headers = {"Authorization": f"Bearer {st.session_state.hf_api_key}"}
        api_url = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
        data = {
            "inputs": {
                "question": prompt,
                "context": "Provide a relevant context here for the question."
            }
        }

        response = requests.post(api_url, headers=headers, json=data)

        # Display the assistant's response if the request was successful.
        if response.status_code == 200:
            assistant_message = response.json().get('answer', "I'm not sure how to answer that.")
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            with st.chat_message("assistant"):
                st.markdown(assistant_message)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
else:
    st.info("Please enter your Hugging Face API key to access the chat.", icon="🗝️")
