import streamlit as st
import requests

# App Title
st.title("Simple Study Chatbot")

# Chat history container
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Backend API URL (update with your backend's actual URL if hosted remotely)
API_URL = "http://127.0.0.1:8000/chat"


# Function to send user messages to the backend
def send_message_to_backend(user_message):
    try:
        # Send a POST request to the backend
        response = requests.post(API_URL, json={"question": user_message})
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response from backend.")
        else:
            return f"Error: Received status code {response.status_code}."
    except Exception as e:
        return f"Error: Unable to reach the backend. {str(e)}"


# Input box for user messages
user_input = st.text_input("You:", placeholder="Type your question here...")

if st.button("Send"):
    if user_input:
        # Add user message to the chat history
        st.session_state.chat_history.append(("You", user_input))

        # Get response from the backend
        bot_response = send_message_to_backend(user_input)

        # Add bot response to the chat history
        st.session_state.chat_history.append(("Bot", bot_response))

        # Clear the input box after sending
        user_input = ""
    else:
        st.warning("Please type a message before sending.")

# Display the chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**{sender}:** {message}")
    else:
        st.markdown(f"_{sender}:_ {message}")