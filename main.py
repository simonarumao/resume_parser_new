import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64
import io

# Configure the Gemini API
genai.configure(api_key="AIzaSyAmLhiM2swlMBGsGE154l6Y1WiDnTMLuCs")

# Function to send data to Gemini API and format the resume
def get_gemini_formatted_resume(user_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([user_data, prompt])
    return response.text

# Function to generate PDF from the formatted resume
def generate_pdf(resume_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split content by lines and add each line to the PDF
    for line in resume_content.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    
    # Create in-memory PDF
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    
    return pdf_output

# Function to download the PDF
def download_pdf(pdf_output, file_name):
    b64 = base64.b64encode(pdf_output.read()).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download Resume PDF</a>'
    return href

# Streamlit UI
st.set_page_config(page_title="Resume Builder with Gemini API")
st.header("AI-Powered Resume Builder")

# User input fields
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
career_objective = st.text_area("Career Objective")
education = st.text_area("Education (e.g., degree, university, year)")
experience = st.text_area("Work Experience (e.g., job title, company, dates, responsibilities)")
skills = st.text_area("Skills (e.g., programming languages, tools)")
projects = st.text_area("Projects (e.g., project name, description, technologies)")
certifications = st.text_area("Certifications (e.g., certification name, issuer)")

# Form the basic resume details into a single user data string
user_data = f"""
Name: {name}
Email: {email}
Phone: {phone}

Career Objective:
{career_objective}

Education:
{education}

Experience:
{experience}

Skills:
{skills}

Projects:
{projects}

Certifications:
{certifications}
"""

# Gemini API prompt to generate a formatted resume
gemini_prompt = """
You are an AI resume formatter. Using the following details provided by the user, format a complete and professional resume.
The sections should include:
1. Name and contact details
2. Career Objective
3. Education
4. Work Experience
5. Skills
6. Projects
7. Certifications
Ensure that the resume follows professional formatting standards and is well-structured.
dont give addition summary at last, do not bold anything and do not bullet also
"""

# Submit button
if st.button("Generate Resume"):
    if name and email and phone:
        # Send data to Gemini and get formatted resume
        formatted_resume = get_gemini_formatted_resume(user_data, gemini_prompt)
        
        # Display the formatted resume in Streamlit
        st.subheader("Formatted Resume")
        st.text_area("Generated Resume", value=formatted_resume, height=300)

        # Generate and download PDF
        pdf_output = generate_pdf(formatted_resume)
        st.markdown(download_pdf(pdf_output, f"{name}_Resume.pdf"), unsafe_allow_html=True)
    else:
        st.error("Please fill in at least your name, email, and phone number.")

