import streamlit as st
import pandas as pd
import os

# File to store feedback
FEEDBACK_FILE = "feedback_data.csv"

# Load admin password from secrets
ADMIN_PASSWORD = st.secrets["admin"]["password"]

# Function to load existing feedback
def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        return pd.read_csv(FEEDBACK_FILE)
    else:
        return pd.DataFrame(columns=[
            "Session Name", "Student Name","Email","USN", "Resource Person", "Topic", "Rating", "Feedback"
        ])

# Function to save feedback
def save_feedback(new_data):
    df = load_feedback()
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)

# Streamlit UI
st.title("📋 Student Feedback Website")

menu = st.sidebar.selectbox("Select Role", ["Student", "Admin"])

if menu == "Student":
    st.subheader("📝 Submit Your Feedback")

    session_name = st.text_input("Name of the Session")
    student_name = st.text_input("Student Name")
    usn = st.text_input("Student USN")
    email=st.text_input("Student Email")
    resource_person = st.text_input("Session Handled by")
    topic = st.text_input("Topic of the Session")
    rating = st.slider("Rating", 1, 5, 1)
    feedback = st.text_area("Feedback")

    if st.button("Submit"):
        if session_name and student_name and usn:
            save_feedback({
                "Session Name": session_name,
                "Student Name": student_name,
                "USN": usn,
                "Email":email,
                "Resource Person": resource_person,
                "Topic": topic,
                "Rating": rating,
                "Feedback": feedback
            })
            st.success("✅ Feedback submitted successfully!")
        else:
            st.warning("⚠ Please fill all the required fields.")

elif menu == "Admin":
    st.subheader("👩‍💻 Admin Panel - Login Required")

    # Password input
    password = st.text_input("Enter Admin Password", type="password")

    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.success("🔓 Access Granted - Welcome Admin!")

            df = load_feedback()
            if not df.empty:
                # --- Filter by Session Name ---
                sessions = df["Session Name"].dropna().unique().tolist()
                selected_session = st.selectbox("🔍 Filter by Session", ["All"] + sessions)

                if selected_session != "All":
                    filtered_df = df[df["Session Name"] == selected_session]
                else:
                    filtered_df = df

                st.dataframe(filtered_df)

                # Download filtered data as CSV
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇ Download Feedback as CSV",
                    data=csv,
                    file_name="feedback_data.csv",
                    mime="text/csv",
                )
            else:
                st.info("No feedback submitted yet.")
        else:
            st.error("❌ Incorrect Password! Access Denied.")