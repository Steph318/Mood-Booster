# streamlit_audio_recorder by stefanrmmr (rs. analytics) - version January 2023

import streamlit as st
from utils import audiorec

# DESIGN implement changes to the standard streamlit UI/UX
# --> optional, not relevant for the functionality of the component!
st.set_page_config(page_title="Chat-to-Boost-your-Mood")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode


def demo_app():

    # TITLE and Creator information
    st.title("🗣️ Speech-to-Speech Chatbot")
    st.markdown('Implemented by '
        '[Damaris](https://www.linkedin.com/in/ndams55/) - '
        'view project source code on '
                
        '[GitHub](https://github.com/Steph318)')
    st.write('\n\n')

    # TUTORIAL: How to use STREAMLIT AUDIO RECORDER?
    # by calling this function an instance of the audio recorder is created
    # once a recording is completed, audio data will be saved to wav_audio_data

    if "hf_api_key" not in st.session_state:
        st.session_state.hf_api_key = st.text_input("Enter Hugging Face API Key", type="password")

    # Si la clé API est définie
    if st.session_state.hf_api_key:
        st.write("Record your question below:")


    wav_audio_data = audiorec() # tadaaaa! yes, that's it! :D

    # add some spacing and informative messages
    col_info, col_space = st.columns([0.57, 0.43])
    with col_info:
        st.write('\n')  # add vertical spacer
        st.write('\n')  # add vertical spacer
        st.write('The .wav audio data, as received in the backend Python code,'
                 ' will be displayed below this message as soon as it has'
                 ' been processed. [This informative message is not part of'
                 ' the audio recorder and can be removed easily] 🎈')

    if wav_audio_data is not None:
        # display audio data as received on the Python side
        col_playback, col_space = st.columns([0.58,0.42])
        with col_playback:
            st.audio(wav_audio_data, format='audio/wav')


if __name__ == '__main__':
    # call main function
    demo_app()
