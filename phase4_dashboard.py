import streamlit as st
from datetime import datetime
import random
import plotly.graph_objects as go
from fpdf import FPDF
import base64

# ---- Constants ---- #
motivational_quotes = [
    "Believe in yourself. You've got this! 💪",
    "Your mind is a garden. Nurture it daily 🌱",
    "Take a deep breath — you're doing great. 🌬️",
    "Every emotion is valid. Let it flow. 🌊",
    "Small steps lead to big change. 🚶‍♂️➡️🏆"
]

goals = [
    "Drink 8 glasses of water 💧",
    "Take a 10-minute mindful walk 🚶‍♀️",
    "Write 3 things you're grateful for ✍️",
    "Avoid social media for 1 hour 📵"
]

mood_numeric = {
    "😊 Happy": 5,
    "😐 Neutral": 3,
    "😰 Anxious": 2,
    "😢 Sad": 1,
    "😠 Angry": 0
}

# ---- PDF Utility ---- #
def generate_pdf(date, mood, note):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Daily Mood Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
    pdf.cell(200, 10, txt=f"Mood: {mood}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Note: {note}")
    return pdf.output(dest="S").encode("latin1")

def download_button(pdf_data, filename="mood_report.pdf"):
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📥 Download Mood Report as PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

# ---- Dashboard Tab ---- #
def show_dashboard():
    st.title("📊 Daily Wellness Dashboard")
    mood_log = st.session_state.get("mood_log", [])

    if not mood_log:
        st.info("📭 No mood data logged yet. Start tracking in the 'Mood Tracker' tab!")
        return

    recent_moods = {}
    for entry in reversed(mood_log):
        day = entry["date"]
        if day not in recent_moods:
            recent_moods[day] = entry["mood"]
        if len(recent_moods) >= 7:
            break

    date_keys = list(recent_moods.keys())[::-1]
    dates = [datetime.strptime(d, "%Y-%m-%d").strftime("%a") for d in date_keys]
    full_labels = [f"{datetime.strptime(d, '%Y-%m-%d').strftime('%b %d')} - {recent_moods[d]}" for d in date_keys]
    mood_labels = list(recent_moods.values())[::-1]
    mood_scores = [mood_numeric.get(mood, 3) for mood in mood_labels]

    today = datetime.today().strftime("%A")
    today_mood = mood_labels[-1] if mood_labels else "😐 Neutral"
    random_quote = random.choice(motivational_quotes)

    # Mood Summary
    st.markdown("### 💫 Today's Mood Summary")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #b2fefa 0%, #0ed2f7 100%); padding: 20px; border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; font-size: 18px; color: #003366;">
        <strong>📅 {today}</strong><br>
        <span style="font-size: 28px; font-weight: bold;">{today_mood}</span><br>
        <em>Your mood matters. Keep nurturing your emotional well-being.</em>
    </div>
    """, unsafe_allow_html=True)

    # Mood Trend Chart
    st.markdown("### 📈 Mood Trend")
    fig = go.Figure(data=go.Scatter(
        x=dates,
        y=mood_scores,
        mode='lines+markers',
        line=dict(color='#00b4d8', width=4),
        text=full_labels,
        hoverinfo='text+y'
    ))
    fig.update_layout(
        yaxis=dict(title='Mood Score (0-5)', range=[0, 5]),
        xaxis=dict(title='Day of Week'),
        height=400,
        plot_bgcolor='#f0f9ff',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Goals Checklist
    st.markdown("### 🎯 Wellness Goals for Today")
    for goal in goals:
        st.markdown(f"""
        <div style="background: #e3f2fd; padding: 12px 18px; border-left: 6px solid #2196f3;
                    border-radius: 12px; font-size: 16px; margin-bottom: 10px; color: #0d47a1;
                    box-shadow: 1px 2px 6px rgba(0,0,0,0.05);">
            ⬜ {goal}
        </div>
        """, unsafe_allow_html=True)

    # Uplifting Reminder
    st.markdown("### 🌟 Uplifting Reminder")
    st.markdown(f"""
    <div style="background: #fff3e0; padding: 20px; border-radius: 15px;
                border: 1px solid #ff9800; font-size: 17px; color: #e65100;
                box-shadow: 0 0 6px rgba(255, 152, 0, 0.2);">
        💬 <em>{random_quote}</em>
    </div>
    """, unsafe_allow_html=True)

# ---- Mood Tracker Tab ---- #
def show_mood_tracker():
    st.title("📝 Daily Mood Tracker")

    with st.form("mood_form"):
        mood = st.radio("How are you feeling today?", list(mood_numeric.keys()), index=1)
        note_input = st.text_area("Write a short note about your day (optional):", key="note_input_form")
        submitted = st.form_submit_button("Submit")

    if submitted:
        today = datetime.today().strftime("%Y-%m-%d")
        new_entry = {"date": today, "mood": mood, "note": note_input}

        if "mood_log" not in st.session_state:
            st.session_state.mood_log = []

        st.session_state.mood_log.append(new_entry)
        st.success("✅ Mood logged successfully!")

        # Store latest note for PDF
        st.session_state.last_note = note_input
        st.session_state.last_mood = mood
        st.session_state.last_date = today

    if "last_mood" in st.session_state:
        st.markdown("### 📄 Download Today's Mood Report")
        pdf_bytes = generate_pdf(
            st.session_state.last_date,
            st.session_state.last_mood,
            st.session_state.last_note
        )
        download_button(pdf_bytes)

# ---- Main App ---- #
st.set_page_config(page_title="MindMates Mood Tracker", layout="centered", page_icon="🧠")
st.sidebar.title("MindMates 🧠")
tab = st.sidebar.radio("Navigate", ["Mood Tracker", "Dashboard"])

if tab == "Mood Tracker":
    show_mood_tracker()
elif tab == "Dashboard":
    show_dashboard()
