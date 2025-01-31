import requests  # noqa: D100
import streamlit as st

st.title("Darija TTS Generator")

# Input text
text = st.text_area("Enter text to convert to speech:", value="السلام عليكم صاحبي")

# Input voice
voice = st.selectbox("Select TTS voice:", ["Male", "Female"])

# Model selection
checkpoint = st.selectbox("Select TTS Model:", [f"states_{i}000" for i in range(6, 7)])

# Generate button
if st.button("Generate Speech"):
	with st.spinner("Generating speech..."):
		try:
			response = requests.post(  # noqa: S113
				"http://localhost:8001/generate",
				json={"text": text, "voice": voice, "checkpoint": checkpoint},
			)
			if response.status_code == 200:  # noqa: PLR2004
				audio_bytes = response.content
				st.audio(audio_bytes, format="audio/wav", autoplay=True)
				st.success("Speech generated successfully!")
			else:
				st.error(f"Error: {response.json().get('detail')}")
		except Exception as e:  # noqa: BLE001
			st.error(f"An error occurred: {e}")
