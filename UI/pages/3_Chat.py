import requests  # noqa: D100
import streamlit as st

st.title("Chat with AI")

# Initialize chat history
if "text_messages" not in st.session_state:
	st.session_state.text_messages = []

# Display chat messages from history on app rerun
for message in st.session_state.text_messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("You:"):
	# Display user message
	st.session_state.text_messages.append({"role": "user", "content": prompt})
	with st.chat_message("user"):
		st.markdown(prompt)

	# Send message to API
	with st.spinner("AI is typing..."):
		try:
			response = requests.post(  # noqa: S113
				"http://localhost:8001/chat",
				json={"messages": st.session_state.text_messages},
			)
			if response.status_code == 200:  # noqa: PLR2004
				reply = response.json().get("response", "")
				st.session_state.text_messages.append(
					{"role": "assistant", "content": reply},
				)
				with st.chat_message("assistant"):
					st.markdown(reply)
			else:
				st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
		except Exception as e:  # noqa: BLE001
			st.error(f"An error occurred: {e}")
