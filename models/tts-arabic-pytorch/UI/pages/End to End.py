import streamlit as st
import requests
import traceback as tb

st.title("End-to-End Voice Chat with AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# remove consecutive messages with same role from messages
def remove_consecutive_messages(messages):
    if len(messages) < 2:
        return messages
    new_messages = [messages[0]]
    for i in range(1, len(messages)):
        if messages[i]["role"] != messages[i - 1]["role"]:
            new_messages.append(messages[i])
    return new_messages

st.session_state.messages = remove_consecutive_messages(st.session_state.messages)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
            st.audio(message.get("audio", None))
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])
            st.audio(message.get("audio", None))

# Chat input for audio
uploaded_audio = st.audio_input("You:")
send = st.button("Send")

if send:
    if uploaded_audio:
        # Display user audio message
        with st.chat_message("user"):
            st.markdown("Audio message")
            st.audio(uploaded_audio)
        
        # Send audio to transcribe endpoint
        with st.spinner("Transcribing your audio..."):
            try:
                files = {"file": uploaded_audio}
                transcribe_response = requests.post("http://localhost:8001/transcribe", files=files)
                if transcribe_response.status_code == 200:
                    transcription = transcribe_response.json().get("transcription", [""])[0]
                    # st.success("Transcription completed!")
                else:
                    st.error(f"Transcription Error: {transcribe_response.json().get('detail')}")
                    transcription = ""
            except Exception as e:
                st.error(f"An error occurred during transcription: {e}")
                transcription = ""
        
        if transcription:
            # Append transcribed text to messages
            st.session_state.messages.append({"role": "user", "content": transcription})
            
            # Send transcribed text to chat endpoint
            with st.spinner("AI is responding..."):
                try:
                    messages = [{"role": message["role"], "content": message["content"]} for message in st.session_state.messages]
                    print(messages)
                    response = requests.post("http://localhost:8001/chat", json={"messages": messages})
                    if response.status_code == 200:
                        reply = response.json().get("response", "")
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    else:
                        st.error(f"Chat Error: {response.json().get('detail', 'Unknown error')}")
                        reply = ""
                except Exception as e:
                    # tb.print_exc()
                    st.error(f"An error occurred while getting AI response: {e}")
                    reply = ""
            
            if reply:
                # Convert AI's reply to speech
                with st.spinner("Converting AI response to speech..."):
                    try:
                        generate_response = requests.post(
                            "http://localhost:8001/generate",
                            json={"text": reply, "voice": "Female", "checkpoint": "states_6000"},
                        )
                        if generate_response.status_code == 200:
                            audio_bytes = generate_response.content
                            st.session_state.messages.append({"role": "assistant", "content": reply, "audio": audio_bytes})
                            with st.chat_message("assistant"):
                                st.audio(audio_bytes, format="audio/wav")
                            # st.success("AI response converted to speech!")
                        else:
                            st.error(f"TTS Error: {generate_response.json().get('detail')}")
                    except Exception as e:
                        st.error(f"An error occurred during TTS conversion: {e}")
    else:
        st.warning("Please upload a WAV file to send.")
