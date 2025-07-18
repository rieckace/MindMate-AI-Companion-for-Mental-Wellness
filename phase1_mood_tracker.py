import streamlit as st
import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def split_text(text, max_chars):
    words = text.split()
    lines, line = [], ""
    for word in words:
        if len(line + " " + word) <= max_chars:
            line += " " + word if line else word
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def generate_summary(logs):
    mood_count = {}
    for entry in logs:
        mood = entry["mood"]
        mood_count[mood] = mood_count.get(mood, 0) + 1
    return mood_count

def generate_pdf(log_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, y, "🧠 MindMates Mood Log Report")
    y -= 20
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, y, f"Generated on: {datetime.datetime.now().strftime('%B %d, %Y - %I:%M %p')}")
    y -= 30

    # Summary
    mood_summary = generate_summary(log_data)
    total_logs = len(log_data)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Total Entries: {total_logs}")
    y -= 20

    p.setFont("Helvetica", 11)
    for mood, count in mood_summary.items():
        p.drawString(70, y, f"{mood}: {count}")
        y -= 15

    y -= 10
    p.line(50, y, width - 50, y)
    y -= 30

    # Log Entries
    p.setFont("Helvetica", 12)
    entry_number = 1
    for entry in reversed(log_data):
        if y < 100:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 12)

        p.setFillColor(colors.darkblue)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, f"{entry_number}. {entry['date']} — {entry['mood']}")
        y -= 20

        if entry['note']:
            p.setFont("Helvetica", 11)
            p.setFillColor(colors.black)
            wrapped_lines = split_text(entry['note'], 85)
            for line in wrapped_lines:
                p.drawString(70, y, "📝 " + line)
                y -= 15
            y -= 5

        p.setFillColor(colors.grey)
        p.line(50, y, width - 50, y)
        y -= 25
        entry_number += 1

    p.save()
    buffer.seek(0)
    return buffer

def show_mood_tracker():
    st.title("🧠 Mood Tracker")

    if "mood_log" not in st.session_state:
        st.session_state["mood_log"] = []

    with st.form("mood_form", clear_on_submit=True):
        moods = ["😊 Happy", "😐 Neutral", "😰 Anxious", "😢 Sad", "😠 Angry"]
        mood = st.radio("How are you feeling today?", moods, horizontal=True)
        note = st.text_area("Would you like to write about it?", placeholder="Share your thoughts...")
        submitted = st.form_submit_button("Log Mood")

        if submitted:
            entry = {
                "date": datetime.date.today().isoformat(),
                "mood": mood,
                "note": note.strip()
            }
            st.session_state["mood_log"].append(entry)
            st.success(f"Mood logged for {entry['date']} — {entry['mood']}")

    if st.session_state["mood_log"]:
        st.markdown("---")
        st.subheader("📅 Mood Log History")

        for entry in reversed(st.session_state["mood_log"]):
            st.markdown(f"""
            <div style="background-color:teal; padding:12px; border-radius:10px; margin-bottom:10px;">
                <strong>{entry['date']}</strong><br>
                Mood: <span style="font-size:18px;">{entry['mood']}</span><br>
                {"📝 " + entry['note'] if entry['note'] else ""}
            </div>
            """, unsafe_allow_html=True)

        # Download PDF button
        pdf = generate_pdf(st.session_state["mood_log"])
        st.download_button(
            label="📥 Download Mood Report as PDF",
            data=pdf,
            file_name="MindMates_Mood_Log.pdf",
            mime="application/pdf"
        )

# Run the app
if __name__ == "__main__":
    show_mood_tracker()
