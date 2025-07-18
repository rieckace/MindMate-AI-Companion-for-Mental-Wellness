import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# Init model
llm = ChatGroq(temperature=0.6, model_name="llama3-8b-8192")

# Prompt template
prompt = PromptTemplate(
    input_variables=["mood"],
    template="""
You're a compassionate AI music therapist. Suggest a type of music or specific song that matches the user's mood,
and explain in 1-2 lines how it helps improve or balance that emotional state.

User's mood: {mood}

Respond with:
1. Music Type or Song Suggestion
2. One sentence therapeutic reason
"""
)

# Create chain
chain = LLMChain(llm=llm, prompt=prompt)

# Mood-to-music mapping
mood_music = {
    "😊 Happy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",  # Pharrell - Happy
    "😢 Sad": "https://www.youtube.com/watch?v=ho9rZjlsyYY",    # Ludovico Einaudi – Nuvole Bianche
    "😠 Angry": "https://www.youtube.com/watch?v=LatorN4P9aA",  # Linkin Park – Numb
    "😰 Anxious": "https://www.youtube.com/watch?v=1ZYbU82GVz4",  # Calming music
    "😐 Neutral": "magical-dramedy-orchestral-sneaky-spell-30-sec-375796.mp3",  # Lo-fi beats
}

def mood_to_music():
    st.header("🎵 Mood-to-Music Companion")
    st.markdown("Let your emotions flow with music chosen just for how you're feeling. 🎧")

    # Check if coming from mood tracker
    auto_mode = False
    selected_mood = None

    if "redirect_to_music" in st.session_state and st.session_state["redirect_to_music"]:
        selected_mood = st.session_state.get("mood", "😐 Neutral")
        auto_mode = True
        # Reset the redirect flag so it doesn't trigger again
        st.session_state["redirect_to_music"] = False
    else:
        selected_mood = st.selectbox("Select your current mood", list(mood_music.keys()))

    # Trigger auto or manual
    if auto_mode or st.button("Get Music & Therapy Insight"):
        with st.spinner("Finding your musical therapy... 🎶"):
            response = chain.run(mood=selected_mood)
            st.video(mood_music[selected_mood])
            st.markdown(f"🧠 **MindMate says:** {response}")
