# import streamlit as st
# import requests

# # Show title and description.
# st.title("💬 Chatbot")
# st.write(
#     "This is a simple chatbot that uses Hugging Face's model to generate responses. "
#     "To use this app, you need to provide a Hugging Face API key once."
# )

# # Ask user for their Hugging Face API key if it's not already stored.
# if "hf_api_key" not in st.session_state:
#     hf_api_key = st.text_input("Hugging Face API Key", type="password")
#     if hf_api_key:
#         # Store the API key in session state and reload to hide the input field.
#         st.session_state.hf_api_key = hf_api_key
#         # st.experimental_rerun()

# # Proceed with the chat interface only if the API key is available in session state.
# if "hf_api_key" in st.session_state:
#     # Initialize chat messages in session state if not already present.
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Display the chat messages stored in session state.
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Chat input for the user.
#     if prompt := st.chat_input("Ask a question based on the context"):
#         # Add user's message to chat history and display it.
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         # Set up Hugging Face API request.
#         headers = {"Authorization": f"Bearer {st.session_state.hf_api_key}"}
#         api_url = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
#         data = {
#             "inputs": {
#                 "question": prompt,
#                 "context": "Provide a relevant context here for the question."
#             }
#         }

#         response = requests.post(api_url, headers=headers, json=data)

#         # Display the assistant's response if the request was successful.
#         if response.status_code == 200:
#             assistant_message = response.json().get('answer', "I'm not sure how to answer that.")
#             st.session_state.messages.append({"role": "assistant", "content": assistant_message})
#             with st.chat_message("assistant"):
#                 st.markdown(assistant_message)
#         else:
#             st.error(f"Error: {response.status_code} - {response.text}")
# else:
#     st.info("Please enter your Hugging Face API key to access the chat.", icon="🗝️")

import streamlit as st
import requests
import streamlit.components.v1 as components
import numpy as np
import soundfile as sf
from io import BytesIO
from pydub import AudioSegment
import base64

st.title("🗣️ Speech-to-Speech Chatbot")

# Check if the API key is entered.
if "hf_api_key" not in st.session_state:
    hf_api_key = st.text_input("Enter Hugging Face API Key", type="password")
    if hf_api_key:
        st.session_state.hf_api_key = hf_api_key
        st.rerun()

# Include only if the API key is set
if "hf_api_key" in st.session_state:
    st.write("Record your question below:")

    

    # Load the HTML file with JavaScript code for audio recording
    with open("audio_recorder.html", "r") as f:
        audio_recorder_html = f.read()
    components.html(audio_recorder_html, height=300)

    # Capture the audio data from the JavaScript
    audio_data = st.session_state.get("audio_data")
    if "audio_data" not in st.session_state:
        st.session_state.audio_data = None

    # Capture audio data from JavaScript
    audio_message = st.query_params.get("audio")
    if audio_message:
        st.session_state.audio_data = audio_message

    if st.session_state.audio_data:
        audio_bytes = BytesIO(base64.b64decode(st.session_state.audio_data.split(",")[1]))
        
        # Convert audio to WAV format, mono, 16kHz (for Whisper ASR)
        audio = AudioSegment.from_file(audio_bytes)
        audio = audio.set_channels(1).set_frame_rate(16000)

        # Save processed audio
        audio_bytes_wav = BytesIO()
        audio.export(audio_bytes_wav, format="wav")
        audio_bytes_wav.seek(0)

        # Display recorded audio for playback
        st.audio(audio_bytes_wav)

        # Transcription
        headers = {"Authorization": f"Bearer {st.session_state.hf_api_key}"}
        whisper_api_url = "https://api-inference.huggingface.co/models/openai/whisper-large"
        response = requests.post(
            whisper_api_url, headers=headers, files={"audio": audio_bytes_wav}
        )

        if response.status_code == 200:
            prompt = response.json().get("text", "")
            st.write("You said:", prompt)

            # Generate response
            qa_api_url = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
            data = {
                "inputs": {
                    "question": prompt,
                    "context": "Provide a relevant context here for the question."
                }
            }
            qa_response = requests.post(qa_api_url, headers=headers, json=data)
            assistant_message = qa_response.json().get('answer', "I'm not sure how to answer that.")
            st.write("Assistant's response:", assistant_message)

            # Text-to-Speech Conversion
            tts_api_url = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"
            tts_response = requests.post(tts_api_url, headers=headers, json={"inputs": assistant_message})

            if tts_response.status_code == 200:
                audio_content = tts_response.content
                st.audio(audio_content, format="audio/wav")
            else:
                st.error("TTS error: Could not generate audio response.")
else:
    st.info("Please enter your Hugging Face API key to continue.")
