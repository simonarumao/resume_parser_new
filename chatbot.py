import streamlit as st
import io
import base64
import pdf2image
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Function to send a prompt and resume content to Gemini
def get_gemini_response(resume_text, user_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([resume_text, user_prompt])
    return response.text

# Extract text from PDF resume
def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()
    return resume_text

# Streamlit UI
st.set_page_config(page_title="Resume Analysis with Gemini")
st.header("Resume Analysis and Q&A with Gemini")

# Resume Upload
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file:
    st.write("PDF Uploaded Successfully")
    resume_text = extract_pdf_text(uploaded_file)
    
    # Text Area for user to input questions
    user_prompt = st.text_area("Ask something about your resume:", key="user_prompt")

    # Button to send request to Gemini
    if st.button("Submit Query"):
        if user_prompt:
            response = get_gemini_response(resume_text, user_prompt)
            st.subheader("Gemini's Response:")
            st.write(response)
        else:
            st.warning("Please enter a prompt/question.")
else:
    st.warning("Please upload your resume.")

