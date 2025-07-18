import streamlit as st
import random
import datetime
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

# Initialize model
llm = ChatGroq(temperature=0.7, model_name="llama3-8b-8192")
memory = ConversationBufferMemory(return_messages=True)

# Daily reset: initialize chat history only if date changed
today_str = datetime.date.today().isoformat()
if st.session_state.get("last_chat_date") != today_str:
    st.session_state["messages"] = []
    st.session_state["last_chat_date"] = today_str

# Mood-aware prompt template
def build_prompt(mood):
    tone_map = {
        "Happy": "cheerful and enthusiastic",
        "Sad": "gentle and compassionate",
        "Anxious": "calming and reassuring",
        "Angry": "soothing and understanding",
        "Calm": "mindful and reflective",
        "Motivated": "encouraging and focused"
    }
    tone = tone_map.get(mood, "friendly and emotionally supportive")

    return PromptTemplate(
        input_variables=["history", "input"],
        template=f"""
You are MindMate 🧠, a supportive AI companion who talks in a {tone} tone based on the user's mood.

Your job is to emotionally support the user through conversation.
You can offer motivational quotes, affirmations, or kind advice when appropriate.

Current conversation:
{{history}}

User: {{input}}
MindMate:
"""
    )

# Add emojis to assistant response
def add_emojis_to_response(text):
    return "🤖 MindMate: " + text.strip()

def ai_companion_chat():
    st.header("🧠 AI Companion Chat - MindMate")
    st.markdown("Feel free to talk to your AI friend. Let it motivate, support, or just listen to you. 💬")

    # ✅ Mood-based tone
    mood = st.session_state.get("mood", "Calm")
    prompt = build_prompt(mood)

    # Use fresh memory every day
    chat = ConversationChain(prompt=prompt, llm=llm, verbose=False, memory=ConversationBufferMemory())

    # Initialize messages list
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle user input
    if user_prompt := st.chat_input("Type your message here..."):
        st.chat_message("user").markdown(user_prompt)

        with st.spinner("MindMate is thinking... 💭"):
            response = chat.predict(input=user_prompt)
            emoji_response = add_emojis_to_response(response)

        # Show response
        st.chat_message("assistant").markdown(emoji_response)

        # Store messages
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.session_state.messages.append({"role": "assistant", "content": emoji_response})
