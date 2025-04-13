import streamlit as st
import fitz  # PyMuPDF
import docx
import os
import google.generativeai as genai

# --- Directly configure API key (⚠️ use env var in production) ---
GEMINI_API_KEY = "AIzaSyAgO5I6sN-2euuM_ZeomQG-ZVZ2EYqEOA4"
genai.configure(api_key=GEMINI_API_KEY)

# --- File Readers ---
def read_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return read_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return read_docx(uploaded_file)
    else:
        return "Unsupported file format. Please upload a .pdf or .docx file."

# --- Google Generative AI Call ---
def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are a resume evaluation expert. Analyze the following resume:
    {resume_text}
    in the context of this job description:
    {job_description}
    Please provide:
    1. An assessment of how well the resume aligns with the job description.
    2. Key strengths of the resume.
    3. Weaknesses or missing elements.
    4. Actionable suggestions to improve alignment.
    5. An alignment rating (1 to 10).
    Answer in structured bullet points.
    """

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text

# --- Streamlit UI ---
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI-Powered Resume Analyzer")

with st.sidebar:
    st.header("Upload Files")
    resume_file = st.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"])
    jd_file = st.file_uploader("Upload Job Description (.pdf or .docx)", type=["pdf", "docx"])

analyze_button = st.button("🔍 Analyze Resume")

if analyze_button and resume_file and jd_file:
    with st.spinner("Extracting text and analyzing..."):
        resume_text = extract_text(resume_file)
        job_text = extract_text(jd_file)
        analysis = analyze_resume(resume_text, job_text)

    st.subheader("📝 Analysis Report")
    st.markdown(analysis)
    st.balloons()

elif analyze_button:
    st.warning("Please upload both resume and job description to proceed.")

# Footer
st.markdown("""
---
Made with ❤️ using Streamlit and Gemini Pro
""")
