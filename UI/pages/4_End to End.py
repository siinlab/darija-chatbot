"""This module provides an end-to-end voice chat application with AI in Darija.

It allows users to upload audio, transcribe it, and get AI responses in both text and
speech.
"""

import requests
import streamlit as st

st.set_page_config(page_title="End-to-End Voice Chat with AI in Darija", layout="wide")


# Initialize chat history and input disabled state
if "messages" not in st.session_state:
	st.session_state.messages = []
if "input_disabled" not in st.session_state:
	st.session_state.input_disabled = False

st.title("End-to-End Voice Chat with AI in Darija")

container = st.container(border=True, height=400)

# Wrap audio_input and send button in a pinned container
uploaded_audio = st.audio_input("You:", disabled=st.session_state.input_disabled)
send = st.button("Send", disabled=st.session_state.input_disabled)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
	with container.chat_message(message["role"]):
		st.write(message["content"])
		audio = message.get("audio", None)
		if audio is not None:
			st.audio(audio)

if send:
	if uploaded_audio:
		st.session_state.input_disabled = True  # Disable audio_input and send button

		# Send audio to transcribe endpoint
		with st.spinner("Transcribing your audio..."):
			try:
				files = {"files": uploaded_audio}
				transcribe_response = requests.post(  # noqa: S113
					"http://localhost:8001/transcribe",
					files=files,
				)
				if transcribe_response.status_code == 200:  # noqa: PLR2004
					transcription = transcribe_response.json()[0]
				else:
					container.error(
						f"Transcription Error: {transcribe_response.json().get('detail')}",  # noqa: E501
					)
					transcription = ""
			except Exception as e:  # noqa: BLE001
				container.error(f"An error occurred during transcription: {e}")
				transcription = ""

		if transcription:
			# display user message
			with container.chat_message("user"):
				st.write(transcription)
				st.audio(uploaded_audio)

			# Append transcribed text to messages
			st.session_state.messages.append(
				{"role": "user", "content": transcription, "audio": uploaded_audio},
			)

			# Send transcribed text to chat endpoint
			with st.spinner("AI is responding..."):
				try:
					messages = [
						{"role": message["role"], "content": message["content"]}
						for message in st.session_state.messages
					]
					response = requests.post(  # noqa: S113
						"http://localhost:8001/chat",
						json={"messages": messages},
					)
					if response.status_code == 200:  # noqa: PLR2004
						reply = response.json()
					else:
						container.error(
							f"Chat Error: {response.json().get('detail', 'Unknown error')}",  # noqa: E501
						)
						reply = ""
				except Exception as e:  # noqa: BLE001
					container.error(f"An error occurred while getting AI response: {e}")
					reply = ""

		if reply:
			# Convert AI's reply to speech
			with st.spinner("Converting AI response to speech..."):
				try:
					generate_response = requests.post(  # noqa: S113
						"http://localhost:8001/generate",
						json={
							"text": reply,
							"voice": "Male",
							"checkpoint": "states_6000",
						},
					)
					if generate_response.status_code == 200:  # noqa: PLR2004
						audio_bytes = generate_response.content
						st.session_state.messages.append(
							{
								"role": "assistant",
								"content": reply,
								"audio": audio_bytes,
							},
						)
						with container.chat_message("assistant"):
							st.write(reply)
							st.audio(audio_bytes, format="audio/wav")
					else:
						container.error(
							f"TTS Error: {generate_response.json().get('detail')}",
						)
				except Exception as e:  # noqa: BLE001
					container.error(f"An error occurred during TTS conversion: {e}")

		st.session_state.input_disabled = False  # Re-enable audio_input and send button
	else:
		container.warning("Please upload a WAV file to send.")
