import streamlit as st
import requests

# Set API key
DEEPSEEK_API_KEY = "sk-1027016b5b8d45f181da11a47bcbf89c"

# Page Config
st.set_page_config(page_title="Tumpa: AI Insurance Chatbot 🤖", layout="wide")

# Title
st.title("Tumpa 🤖 - Your Insurance Chat Assistant")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to display a single chat message with left/right alignment
def display_chat(role, content):
    if role == "user":
        col1, col2 = st.columns([0.4, 0.6])
        with col2:
            st.markdown(f"""
            <div style='background-color:#DCF8C6; padding:10px; border-radius:10px; text-align:right;'>
                <strong>You:</strong><br>{content}
            </div>
            """, unsafe_allow_html=True)
    elif role == "assistant":
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            st.markdown(f"""
            <div style='background-color:#F1F0F0; padding:10px; border-radius:10px; text-align:left;'>
                <strong>Tumpa 🤖:</strong><br>{content}
            </div>
            """, unsafe_allow_html=True)

# Display chat history
for chat in st.session_state.chat_history:
    display_chat(chat["role"], chat["content"])

# Chat input box (bottom of screen)
query = st.chat_input("Ask about insurance policies...")

# When a message is sent
if query:
    # Add user input to history
    st.session_state.chat_history.append({"role": "user", "content": query})

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [{"role": "system", "content": "You are a helpful assistant for insurance policies."}] + st.session_state.chat_history

    data = {
        "model": "deepseek-chat",
        "messages": messages
    }
    response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = f"❌ Error {response.status_code}: {response.text}"
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()


# if there any kind of issue with that api key then please don't underestimate my code ...it will definetly working model