import streamlit as st
import random
import pandas as pd
import os
import datetime

ROUTINE_FILE = "routines.csv"

# Simulated mood context
def get_user_context():
    moods = ['Happy', 'Sad', 'Anxious', 'Calm', 'Angry', 'Motivated']
    return random.choice(moods)

# Generate AI-based tips
def generate_wellness_tips(mood):
    tips_database = {
        "Happy": [
            "Keep a gratitude journal to savor the good moments 🌼",
            "Spread positivity — compliment someone today 😊",
            "Go outdoors and soak in some sunshine ☀️"
        ],
        "Sad": [
            "Try journaling how you feel — let it all out 💙",
            "Watch your comfort movie or talk to someone you trust 🎬",
            "Take a short walk to boost your mood 🚶‍♀️"
        ],
        "Anxious": [
            "Practice box breathing (4-4-4-4) for 2 minutes 🧘‍♂️",
            "Limit social media for a few hours 📵",
            "Try progressive muscle relaxation 💪"
        ],
        "Calm": [
            "Use this calm to do something creative 🎨",
            "Practice mindfulness or silent sitting 🙏",
            "Listen to ambient music and relax 🎵"
        ],
        "Angry": [
            "Try writing a ‘no-send’ letter to vent 🔥",
            "Engage in physical activity like jumping jacks 🏃",
            "Splash cold water on your face or hands ❄️"
        ],
        "Motivated": [
            "Channel your energy into a passion project 🚀",
            "Start your day with a prioritized to-do list ✅",
            "Set a mini-goal and crush it today 💯"
        ]
    }
    return random.sample(tips_database[mood], 2)

# Save selected routine to CSV
def save_routine(date, selected_activities):
    df = pd.DataFrame({
        "date": [date] * len(selected_activities),
        "activity": selected_activities
    })

    if os.path.exists(ROUTINE_FILE):
        existing = pd.read_csv(ROUTINE_FILE)
        # Remove existing entry for today before saving
        existing = existing[existing["date"] != date]
        df = pd.concat([existing, df], ignore_index=True)

    df.to_csv(ROUTINE_FILE, index=False)

# Load routine for today
def load_today_routine(date):
    if os.path.exists(ROUTINE_FILE):
        df = pd.read_csv(ROUTINE_FILE)
        today_activities = df[df["date"] == date]["activity"].tolist()
        return today_activities
    return []

# Daily routine builder UI
def build_routine(date):
    st.subheader("🗓️ Build Your Daily Wellness Routine")

    default_options = [
        "🌞 Morning Meditation",
        "📓 Journaling",
        "🚶‍♂️ Light Walk or Yoga",
        "📴 Digital Detox Time",
        "🫶 Affirmations",
        "🎧 Music Therapy",
        "🌿 Mindful Eating",
        "🧘‍♂️ Meditate"
    ]

    if "routine_data" not in st.session_state:
        st.session_state.routine_data = {activity: False for activity in load_today_routine(date)}

    # Show existing activities with checkbox to mark complete
    if st.session_state.routine_data:
        st.success("✅ Your saved routine for today:")
        to_delete = []
        for activity, completed in st.session_state.routine_data.items():
            cols = st.columns([0.08, 0.82, 0.1])
            with cols[0]:
                st.session_state.routine_data[activity] = st.checkbox("", value=completed, key=f"check_{activity}")
            with cols[1]:
                st.markdown(f"{'✅' if completed else '🔲'} {activity}")
            with cols[2]:
                if cols[2].button("❌", key=f"delete_{activity}"):
                    to_delete.append(activity)
        # Handle deletions
        for act in to_delete:
            st.session_state.routine_data.pop(act)

    # Add custom activity
    st.markdown("---")
    st.markdown("**➕ Add a New Activity:**")
    if "new_activity" not in st.session_state:
        st.session_state.new_activity = ""
    new_activity = st.text_input("Type your custom activity:", value=st.session_state.new_activity, key="new_activity_input")
    if st.button("➕ Add Activity"):
        if new_activity.strip():
            st.session_state.routine_data[new_activity.strip()] = False
            st.session_state.new_activity = ""  # clear input
            st.success(f"Added: {new_activity.strip()}")
            st.rerun()

    # Save
    st.markdown("---")
    if st.button("💾 Save Today's Routine"):
        save_routine(date, list(st.session_state.routine_data.keys()))
        st.success("Routine saved successfully! ✅")

# Main Phase 5 function
def show_wellness_tips():
    st.title("🌟 Personalized Wellness Tips")

    date_today = datetime.date.today().isoformat()
    mood = get_user_context()
    st.markdown(f"**Based on your current mood:** _{mood}_ 💬")

    tips = generate_wellness_tips(mood)
    st.subheader("💡 Wellness Tips for You")
    for tip in tips:
        st.markdown(f"- {tip}")

    if st.button("🔄 Get Fresh Tips"):
        st.rerun()

    build_routine(date_today)
