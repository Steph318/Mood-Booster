# Streamlit Audio Recorder

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://audiorecorder.streamlit.app/)
[![Generic badge](https://img.shields.io/badge/PyPI-pip_install_streamlit--audiorec-black.svg)](https://pypi.org/project/streamlit-audiorec/)
[![Generic badge](https://img.shields.io/badge/Package-v0.1.3-blue.svg)](https://pypi.org/project/streamlit-audiorec/)
[![GitHub license](https://img.shields.io/badge/Licence-MIT-gr.svg)](https://github.com/stefanrmmr/streamlit-audio-recorder/blob/main/LICENCE)


Implemented by [Damaris](https://www.linkedin.com/in/ndams55/), <br/>


## Features & Specs
- [It will come] **browser's Media-API**<br>

## Setup & How to Use
**1.** PIP Install the component (download from PyPI)
```
pip install streamlit-audiorec
```
**2.** Import and Initialize the component (at the top of your script)
```python
from utils import audiorec
```
**3.** Add an Instance of the audio recorder to your streamlit app's code.
```python 
wav_audio_data = audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')
```
**4. HAVE A FUN! 🎈**

Feel free to reach out to me in case you have any questions! <br>
Pls consider leaving a `star` ☆ with this repository to show your support.
