import requests  # noqa: D100
import streamlit as st

st.title("Transcribe Audio")

uploaded_file = st.file_uploader("Upload a WAV file for transcription", type=["wav"])
recorded_file = st.audio_input("Record an audio")

if st.button("Transcribe"):
	if uploaded_file is not None or recorded_file is not None:
		if uploaded_file is None:
			uploaded_file = recorded_file
		with st.spinner("Transcribing audio..."):
			try:
				files = {"files": uploaded_file}
				response = requests.post(  # noqa: S113
					"http://localhost:8001/transcribe",
					files=files,
				)
				if response.status_code == 200:  # noqa: PLR2004
					transcription = response.json()[0]
					st.write(f"Transcription: {transcription}")
					st.success("Transcription completed successfully!")
				else:
					st.error(f"Error: {response.json().get('detail')}")
			except Exception as e:  # noqa: BLE001
				st.error(f"An error occurred: {e}")
	else:
		st.warning("Please upload a WAV file before transcribing.")
