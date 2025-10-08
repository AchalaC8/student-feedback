import streamlit as st
import pandas as pd
import mysql.connector
import os

# DB connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Chandu@123"),
        database=os.getenv("DB_NAME", "feed")
    )

# Admin password from env or secrets
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or st.secrets["admin"]["password"]

# ---------------------- DB Functions ----------------------
def load_feedback():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedback")
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows)

def save_feedback(new_data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO feedback (session_name, student_name, usn, email, resource_person, topic, rating, feedback)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(sql, (
        new_data["Session Name"], new_data["Student Name"], new_data["USN"],
        new_data["Email"], new_data["Resource Person"], new_data["Topic"],
        new_data["Rating"], new_data["Feedback"]
    ))
    conn.commit()
    conn.close()

def load_sessions():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sessions")
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows)

def save_session(session_name, resource_person, topic):
    conn = get_connection()
    cursor = conn.cursor()
    # Check duplicate
    cursor.execute(
        "SELECT * FROM sessions WHERE session_name=%s AND resource_person=%s AND topic=%s",
        (session_name, resource_person, topic)
    )
    duplicate = cursor.fetchall()
    if duplicate:
        conn.close()
        return False
    sql = "INSERT INTO sessions (session_name, resource_person, topic) VALUES (%s, %s, %s)"
    cursor.execute(sql, (session_name, resource_person, topic))
    conn.commit()
    conn.close()
    return True

# ---------------------- UI ----------------------
st.set_page_config(page_title="Student Feedback Portal", layout="centered")
st.markdown("<h1 style='text-align: center;'>🎓 Student Feedback Portal</h1>", unsafe_allow_html=True)

if "last_role" not in st.session_state:
    st.session_state.last_role = None
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

menu = st.sidebar.radio("Choose Role", ["Student", "Admin"])

if menu != st.session_state.last_role:
    st.session_state.admin_logged_in = False
    st.session_state.last_role = menu

# ---------------------- STUDENT PANEL ----------------------
if menu == "Student":
    st.markdown("### 📝 Submit Your Feedback")

    session_df = load_sessions()

    if not session_df.empty:
        session_names = session_df["session_name"].dropna().unique().tolist()
        selected_session = st.selectbox("Select Session", [""] + session_names)

        if selected_session:
            filtered_df = session_df[session_df["session_name"] == selected_session]
            resource_options = filtered_df["resource_person"].dropna().unique().tolist()
            topic_options = filtered_df["topic"].dropna().unique().tolist()

            selected_resource = st.selectbox("Select Resource Person", [""] + resource_options)
            selected_topic = st.selectbox("Select Topic of the Session", [""] + topic_options)

            col1, col2 = st.columns(2)
            with col1:
                student_name = st.text_input("Student Name")
                usn = st.text_input("Student USN")
            with col2:
                email = st.text_input("Student Email")
                rating = st.slider("Rating", 1, 5, 3)

            feedback = st.text_area("Feedback", height=150)

            st.markdown("---")
            if st.button("📨 Submit Feedback"):
                if student_name and usn and email and feedback and selected_resource and selected_topic:
                    save_feedback({
                        "Session Name": selected_session,
                        "Student Name": student_name,
                        "USN": usn,
                        "Email": email,
                        "Resource Person": selected_resource,
                        "Topic": selected_topic,
                        "Rating": rating,
                        "Feedback": feedback
                    })
                    st.success("✅ Feedback submitted successfully!")
                else:
                    st.warning("⚠️ Please fill all the required fields.")
        else:
            st.info("Please select a session to continue.")
    else:
        st.info("No sessions available yet. Please check back later.")

# ---------------------- ADMIN PANEL ----------------------
elif menu == "Admin":
    st.markdown("### 🔐 Admin Panel")

    if not st.session_state.admin_logged_in:
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("🔓 Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Access Granted")
            else:
                st.error("❌ Incorrect Password")

    if st.session_state.admin_logged_in:
        st.success("Welcome, Admin!")

        st.markdown("### ➕ Add New Session")
        col1, col2 = st.columns(2)
        with col1:
            new_session = st.text_input("Session Name")
            new_resource_person = st.text_input("Resource Person")
        with col2:
            new_topic = st.text_input("Topic of the Session")

        if st.button("➕ Add Session"):
            if new_session and new_resource_person and new_topic:
                success = save_session(new_session, new_resource_person, new_topic)
                if success:
                    st.success("✅ Session added successfully!")
                else:
                    st.warning("⚠️ This exact session already exists.")
            else:
                st.warning("⚠️ Please fill all fields.")

        st.markdown("### 📊 View Submitted Feedback")
        df = load_feedback()
        if not df.empty:
            sessions = df["session_name"].dropna().unique().tolist()
            selected_session = st.selectbox("Filter by Session", ["All"] + sessions)

            filtered_df = df if selected_session == "All" else df[df["session_name"] == selected_session]
            st.dataframe(filtered_df, use_container_width=True)

            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇ Download Feedback as CSV",
                data=csv,
                file_name="feedback_data.csv",
                mime="text/csv",
            )
        else:
            st.info("No feedback submitted yet.")
