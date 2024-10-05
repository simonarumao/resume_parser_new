import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64
import io
import pdf2image
from PIL import Image

# Configure the Gemini API
genai.configure(api_key="AIzaSyAmLhiM2swlMBGsGE154l6Y1WiDnTMLuCs")

# ---- Resume Maker Functions ---- #
def get_gemini_formatted_resume(user_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([user_data, prompt])
    return response.text

def generate_pdf(resume_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Adding the resume content line by line
    for line in resume_content.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    
    # Write PDF content to BytesIO object
    pdf_output = io.BytesIO()
    
    # Output PDF to the BytesIO object (using dest='S' for stream)
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    
    # Move the file pointer to the beginning of the BytesIO object
    pdf_output.seek(0)
    
    return pdf_output


def download_pdf(pdf_output, file_name):
    b64 = base64.b64encode(pdf_output.read()).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download Resume PDF</a>'
    return href

# ---- Resume Analyzer Functions ---- #
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    first_page = images[0]
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
    return pdf_parts

# ---- Streamlit UI ---- #
st.set_page_config(page_title="AI-Powered Resume Tool")

# Sidebar for navigation
option = st.sidebar.selectbox("Choose an option:", ("Resume Maker", "Resume Analyzer","Cover Letter Generator","Interview Prep"))

# Resume Maker
if option == "Resume Maker":
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

    # Combine user data
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

    gemini_prompt = """
    You are an AI resume formatter. Using the following details provided by the user, format a complete and professional resume.
    Ensure that the resume follows professional formatting standards and is well-structured.
    Do not bold anything and avoid using bullets.
    """

    # Generate Resume Button
    if st.button("Generate Resume"):
        if name and email and phone:
            formatted_resume = get_gemini_formatted_resume(user_data, gemini_prompt)
            st.subheader("Formatted Resume")
            st.text_area("Generated Resume", value=formatted_resume, height=300)

            pdf_output = generate_pdf(formatted_resume)
            st.markdown(download_pdf(pdf_output, f"{name}_Resume.pdf"), unsafe_allow_html=True)
        else:
            st.error("Please fill in at least your name, email, and phone number.")

# Resume Analyzer
elif option == "Resume Analyzer":
    st.header("Resume Review System")

    # Job Description and File Upload
    input_text = st.text_area("Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")

    # Analyzer buttons
    if st.button("Tell me About the Resume"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, "Provide a detailed review of this resume.")
            st.subheader("Resume Review")
            st.write(response)
        else:
            st.error("Please upload a resume.")

    if st.button("Compare Resume with Job Description"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, "Compare the resume with the job description.")
            st.subheader("Comparison")
            st.write(response)
        else:
            st.error("Please upload a resume.")

    if st.button("Identify Missing Skills"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, "Identify missing skills in the resume based on the job description.")
            st.subheader("Missing Skills")
            st.write(response)
        else:
            st.error("Please upload a resume.")
    
    if st.button("Percentage Match"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, '''You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
                                    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
                                    the job description. First the output should come as percentage and then keywords missing and last final thoughts.Highlight the missing keywords in bold.''')
            st.subheader("Percentage Match")
            st.write(response)
        else:
            st.error("Please upload a resume.")

    if st.button("Interview question on Resume and JD"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, """You are an AI interview coach. Generate potential interview questions that the candidate should prepare for based on the following resume and job description.""")
            st.subheader("Interview question on Resume and JD")
            st.write(response)
        else:
            st.error("Please upload a resume.")

elif option == "Cover Letter Generator":
    st.header("Cover Letter Generator")

    input_text = st.text_area("Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")


    if st.button("Create a Cover Letter"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, "Provide a detailed Cover letter based on this resume and job description. take name and everything from resume")
            st.subheader("Cover Letter")
            st.write(response)
        else:
            st.error("Please upload a resume.")



elif option == "Interview Prep":
    st.header("Interview Prep")

    input_text = st.text_area("Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")


    if st.button("Ask Question"):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, "Give me a list of questions based on my resume and the job descrition provided with expected answers.Dont just give regarding job description also give resume based.")
            st.subheader("Interview Questions")
            st.write(response)
        else:
            st.error("Please upload a resume.")

    

    
