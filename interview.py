import streamlit as st
import time
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Interview Schedule | XYZ Corp", page_icon="🗓️", layout="centered")

# Title and welcome message
st.title("🎉 Interview Scheduler - XYZ Corp")
st.markdown("Welcome to the official interview portal of **XYZ Corp**.\n\nPlease fill in the details below to confirm your interview.")

# Form Inputs
with st.form("interview_form", clear_on_submit=False):
    st.subheader("👤 Candidate Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Mobile Number")
    position = st.text_input("Position Applied For")

    st.subheader("📅 Interview Slot")
    interview_date = st.date_input("Select Interview Date")
    interview_time = st.time_input("Select Interview Time")

    submitted = st.form_submit_button("✅ Schedule Interview")

# Show confirmation popup
if submitted:
    if all([name, email, phone, position]):
        with st.spinner("Scheduling your interview..."):
            time.sleep(2)
        interview_datetime = datetime.combine(interview_date, interview_time)
        st.success(f"🎯 Your interview has been scheduled on **{interview_datetime.strftime('%A, %B %d, %Y at %I:%M %p')}**.")
        st.balloons()
        st.markdown(f"""
        ---
        📩 A confirmation email will be sent to **{email}**.  
        📞 Please be available on **{phone}** at the time of your interview.

        💻 The interview will be conducted via **Microsoft Teams**.  
        🔗 The link will be shared with you **just before the interview day**.

        🔁 You can revisit this page if you'd like to reschedule.
        """)
    else:
        st.warning("⚠️ Please fill in all fields before submitting.")

