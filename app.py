import streamlit as st
import spacy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import PyPDF2
from docx import Document
import time
from datetime import datetime
import subprocess
import sys

# Ensure spaCy model is available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Read PDF
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "".join([page.extract_text() for page in reader.pages])

# Read DOCX
def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Extract keywords
def extract_keywords(text):
    doc = nlp(text.lower())
    return set(token.lemma_ for token in doc if token.is_alpha and not token.is_stop and token.text not in ENGLISH_STOP_WORDS)

# Match skills
def match_resume_skills(resume_text, job_keywords):
    resume_keywords = extract_keywords(resume_text)
    return resume_keywords.intersection(job_keywords)

# Streamlit page setup
st.set_page_config(page_title="AI Job Screening System | XYZ Corp", layout="centered")
st.title("🎯 AI Job Screening System - XYZ Corp")

# Step 1: Job Description
st.subheader("📌 Paste Job Description")
jd_text = st.text_area("Paste the full job description:")

job_keywords = set()
if jd_text:
    job_keywords = extract_keywords(jd_text)
    st.success("✅ Job description processed successfully!")

# Step 2: Resume Upload
st.subheader("📤 Upload Your Resume")
resume_file = st.file_uploader("Upload a PDF or DOCX resume", type=["pdf", "docx"])

if resume_file and job_keywords:
    resume_text = read_pdf(resume_file) if resume_file.type == "application/pdf" else read_docx(resume_file)
    matched = match_resume_skills(resume_text, job_keywords)

    if matched:
        st.markdown("### ✅ Skills Matched:")
        st.success(", ".join(sorted(matched)))
        st.balloons()
        st.markdown("## 🟢 Congratulations! You're selected for the interview round!")

        # Interview Scheduler
        st.markdown("---")
        st.header("📅 Interview Scheduler - XYZ Corp")
        st.markdown("Please confirm your interview details below:")

        with st.form("interview_form", clear_on_submit=False):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Mobile Number")
            position = st.text_input("Position Applied For")
            interview_date = st.date_input("Preferred Interview Date")
            interview_time = st.time_input("Preferred Interview Time")
            submitted = st.form_submit_button("✅ Schedule Interview")

        if submitted:
            if all([name, email, phone, position]):
                with st.spinner("⏳ Scheduling your interview..."):
                    time.sleep(2)
                interview_datetime = datetime.combine(interview_date, interview_time)
                st.success(f"🎯 Interview Scheduled: **{interview_datetime.strftime('%A, %B %d, %Y at %I:%M %p')}**")
                st.balloons()
                st.markdown(f"""
                ---
                📩 Confirmation will be sent to **{email}**  
                📞 Be available on **{phone}** at the scheduled time  
                💻 Interview via **Microsoft Teams**  
                🔗 Link shared a day before the interview
                """)
            else:
                st.warning("⚠️ Please fill in all fields before submitting.")
    else:
        st.markdown("### ❌ No Relevant Skills Found")
        st.error("🔴 Sorry! You're not shortlisted for the interview based on the provided job description.")
