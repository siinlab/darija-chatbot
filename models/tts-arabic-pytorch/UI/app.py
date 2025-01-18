import streamlit as st
import requests
import os

st.title("Darija TTS Generator")

# Input text
text = st.text_area("Enter text to convert to speech:", value="السلام عليكم صاحبي")

# Model selection
model_name = st.selectbox("Select TTS Model:", ["states_6000", "states_7000"])

# Generate button
if st.button("Generate Speech"):
	with st.spinner("Generating speech..."):
		try:
			response = requests.post(
				"http://localhost:8001/generate",
				json={"text": text, "model_name": model_name},
			)
			if response.status_code == 200:
				audio_bytes = response.content
				st.audio(audio_bytes, format="audio/wav")
				st.success("Speech generated successfully!")
			else:
				st.error(f"Error: {response.json().get('detail')}")
		except Exception as e:
			st.error(f"An error occurred: {e}")
