import streamlit as st
import spacy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import PyPDF2
from docx import Document
import time
from datetime import datetime

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# PDF reader
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# DOCX reader
def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Keyword extraction
def extract_keywords(text):
    doc = nlp(text.lower())
    return set(token.lemma_ for token in doc if token.is_alpha and not token.is_stop and token.text not in ENGLISH_STOP_WORDS)

# Resume vs JD keyword matcher
def match_resume_skills(resume_text, job_keywords):
    resume_keywords = extract_keywords(resume_text)
    return resume_keywords.intersection(job_keywords)

# Streamlit page config
st.set_page_config(page_title="AI Job Screening System | XYZ Corp", layout="centered")
st.title("🎯 AI Job Screening System - XYZ Corp")

# Step 1: Job Description
st.subheader("📌 Paste Job Description")
jd_text = st.text_area("Enter the full job description here:")

job_keywords = set()
if jd_text:
    job_keywords = extract_keywords(jd_text)
    st.success("✅ Job Description processed.")

# Step 2: Resume Upload
st.subheader("📤 Upload Resume")
resume_file = st.file_uploader("Upload a resume file (PDF or DOCX)", type=["pdf", "docx"])

if resume_file and job_keywords:
    resume_text = read_pdf(resume_file) if resume_file.type == "application/pdf" else read_docx(resume_file)
    matched = match_resume_skills(resume_text, job_keywords)

    if matched:
        st.markdown("### ✅ Skills Matched:")
        st.success(", ".join(sorted(matched)))
        st.balloons()
        st.markdown("## 🟢 You are SELECTED for the Interview Round!")

        # Interview Scheduling Form
        st.markdown("---")
        st.header("📅 Interview Scheduler - XYZ Corp")
        st.markdown("Please fill in the details below to confirm your interview.")

        with st.form("interview_form", clear_on_submit=False):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Mobile Number")
            position = st.text_input("Position Applied For")

            interview_date = st.date_input("Select Interview Date")
            interview_time = st.time_input("Select Interview Time")

            submitted = st.form_submit_button("✅ Schedule Interview")

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

                💻 The interview will be conducted via **Microsoft Teams**.  
                🔗 The link will be shared with you **just before the interview day**.

                🔁 You can revisit this page if you'd like to reschedule.
                """)
            else:
                st.warning("⚠️ Please fill in all fields before submitting.")
    else:
        st.markdown("### ❌ No Relevant Skills Found")
        st.error("🔴 You are REJECTED based on the job description.")

# Contact Team Section
st.markdown("---")
st.header("📬 Contact the Team")

with st.form("contact_form", clear_on_submit=True):
    st.text_input("Name", value="SUPRIYA MANDAL", disabled=True)
    st.text_input("Email", value="anisupriya2002@gmail.com", disabled=True)
    message = st.text_area("Your Message (Max 500 characters)", max_chars=500)
    attachment = st.file_uploader("Upload File (optional)", type=["pdf", "docx", "txt"])

    submitted_contact = st.form_submit_button("📨 Send Message")

    if submitted_contact:
        if message.strip():
            st.success("✅ Message sent to the team successfully!")
            st.info("📩 You will receive a response at anisupriya2002@gmail.com.")
        else:
            st.warning("⚠️ Message box cannot be empty.")
