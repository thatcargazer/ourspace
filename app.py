import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
st.set_page_config(page_title="💛 Our Little Space", layout="centered")

PASSWORD = "nammadhaan"  # change this 💛
START_TIME = datetime(2025, 12, 27, 2, 8)

# ---------------- DB SETUP ----------------
conn = sqlite3.connect("ldr.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS counters (
    name TEXT PRIMARY KEY,
    count INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS updates (
    type TEXT,
    value TEXT,
    timestamp TEXT
)
""")

for key in ["rawrrrrr", "miss_youuu", "kissy", "huggiess"]:
    c.execute("INSERT OR IGNORE INTO counters VALUES (?, ?)", (key, 0))

conn.commit()

# ---------------- STYLING ----------------
st.markdown("""
<style>
body {
    background-color: #FFF7CC;
}
.main {
    background-color: #FFF7CC;
}
button {
    border-radius: 20px !important;
    height: 3em;
}
h1, h2, h3 {
    color: #6B4F00;
}
.card {
    background: #FFEB99;
    padding: 15px;
    border-radius: 20px;
    margin-bottom: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- AUTH ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Private Space")
    pwd = st.text_input("Password", type="password")
    if st.button("Enter 💛"):
        if pwd == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Wrong password, go ask sodala 🥺")
    st.stop()

# ---------------- HEADER ----------------
st.title("💛 Our Little World")

# ---------------- LOVE TIMER ----------------
now = datetime.now()
delta = now - START_TIME

days = delta.days
hours, remainder = divmod(delta.seconds, 3600)
minutes, seconds = divmod(remainder, 60)

st.markdown(
    f"""
    <div class="card">
    🕰️ <b>We chose each other</b><br>
    {days} days • {hours} hrs • {minutes} mins • {seconds} secs ago 💛
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- COUNTER BUTTONS ----------------
st.subheader("Send Some Love")

cols = st.columns(4)
buttons = [
    ("🦖 Rawrrrrr", "rawrrrrr"),
    ("🥺 Miss youuu", "miss_youuu"),
    ("💋 Kissy", "kissy"),
    ("🤗 Huggiess", "huggiess"),
]

for col, (label, key) in zip(cols, buttons):
    with col:
        if st.button(label):
            c.execute("UPDATE counters SET count = count + 1 WHERE name = ?", (key,))
            conn.commit()

# Show counts
c.execute("SELECT name, count FROM counters")
counts = dict(c.fetchall())

st.markdown(
    f"""
    <div class="card">
    🦖 Rawrrrrr: {counts['rawrrrrr']}<br>
    🥺 Miss youuu: {counts['miss_youuu']}<br>
    💋 Kissy: {counts['kissy']}<br>
    🤗 Huggiess: {counts['huggiess']}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- GOOD MORNING / NIGHT ----------------
st.subheader("🌞🌙 Daily Check-ins")

col1, col2 = st.columns(2)

with col1:
    if st.button("🌞 Good Morning"):
        c.execute(
            "INSERT INTO updates VALUES (?, ?, ?)",
            ("greeting", "Good Morning", datetime.now().isoformat())
        )
        conn.commit()

with col2:
    if st.button("🌙 Good Night"):
        c.execute(
            "INSERT INTO updates VALUES (?, ?, ?)",
            ("greeting", "Good Night", datetime.now().isoformat())
        )
        conn.commit()

c.execute("""
SELECT value, timestamp FROM updates
WHERE type='greeting'
ORDER BY timestamp DESC LIMIT 1
""")
last_greet = c.fetchone()

if last_greet:
    st.info(f"💬 Last: **{last_greet[0]}** at {last_greet[1][:16]}")

# ---------------- MEAL UPDATES ----------------
st.subheader("🍽️ Meal Updates")

meal_cols = st.columns(3)
meals = ["Breakfast 🍳", "Lunch 🍛", "Dinner 🍜"]

for col, meal in zip(meal_cols, meals):
    with col:
        if st.button(meal):
            c.execute(
                "INSERT INTO updates VALUES (?, ?, ?)",
                ("meal", meal, datetime.now().isoformat())
            )
            conn.commit()

c.execute("""
SELECT value, timestamp FROM updates
WHERE type='meal'
ORDER BY timestamp DESC LIMIT 1
""")
last_meal = c.fetchone()

if last_meal:
    st.success(f"🍴 Last meal: **{last_meal[0]}** at {last_meal[1][:16]}")

# ---------------- FOOTER ----------------
st.markdown("""
---
💛 *Haan Vaalthukkal Vaalthukkal.*  
🫂 *Nammadhaaan.*
""")
