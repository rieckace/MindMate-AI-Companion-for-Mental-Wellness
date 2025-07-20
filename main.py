#All the necesaary imports are here 
import streamlit as st
from phase1_mood_tracker import show_mood_tracker
from phase2_journal_coping import mood_journal_and_coping_tools
from phase3_ai_companion import ai_companion_chat
from phase4_dashboard import show_dashboard
from phase5_personalized_tips import show_wellness_tips
from phase6_mood_music import mood_to_music

# Page configuration
st.set_page_config(page_title="MindMate", layout="centered")
st.title("🧘 MindMate: Your AI Companion for Mental Wellness")

# Determine which tab to activate
default_tab_index = 1 if st.session_state.get("redirect_to_music") else 0

tabs = st.tabs([
    "📍 Mood Tracker",
    "🎵 Mood Music",
    "📔 Journal & Coping",
    "🧠 AI Companion",
    "🏠 Dashboard",
    "🌟 Wellness Tips"
])

tab1, tab2, tab3, tab4, tab5, tab6 = tabs

# Phase 1
with tab1:
    show_mood_tracker()

# Phase 6 - Auto-play based on redirected mood
with tab2:
    mood_to_music()

# Phase 2
with tab3:
    mood_journal_and_coping_tools()

# Phase 3
with tab4:
    ai_companion_chat()

# Phase 4
with tab5:
    show_dashboard()

# Phase 5
with tab6:
    show_wellness_tips()

# Reset redirect after switching
if st.session_state.get("redirect_to_music"):
    st.session_state.redirect_to_music = False
