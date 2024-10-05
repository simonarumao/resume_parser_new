
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
from pdf2image import convert_from_bytes
import google.generativeai as genai

genai.configure(api_key = "AIzaSyAmLhiM2swlMBGsGE154l6Y1WiDnTMLuCs")


def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    #conver the pdf to image

    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title = "ATS RESUME EXPERT")

st.header("RESUME REVIEW SYSTEM")

input_text = st.text_area("Job Description:",key="input")

uploaded_file = st.file_uploader("Upload Your resume(PDF)",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me About the Resume")

submit2 = st.button("Explain job description")

submit4 = st.button("Compare the Resume")

submit7 = st.button("Errors in resume")

submit5 = st.button("Identify Missing skills")

submit6 = st.button("Interview question on Resume and JD")

submit3 = st.button("Percentage Match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """You are an AI language model. Analyze the following job description and summarize the key skills, qualifications, and responsibilities required.Explain the job description in simple manner """

input_prompt4 = """You are an skilled AI resume evaluator. Compare the candidate's resume with the provided job description.
1. Gaps Identified: List the key areas where the resume falls short compared to the job description. You can keep it short and useful"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.Highlight the missing keywords in bold.
"""
input_prompt7 = """You are an AI resume evaluator. Review the following resume for any errors or improvements in the following areas:
1. Grammatical Errors: Identify and list any grammatical and spelling mistakes.
2. Structural Issues: Check for consistency in formatting, font usage, and layout.
3. Chronological Errors: Verify the chronological order of experiences, education, and other relevant sections
clearly look for any spelling mistakes and point them out, look for dates if right and lastly list what is wrong.
if there are not at all error then u can specifiy no error, but if there then show them"""
input_prompt5 = """"You are an AI evaluator. Identify any key skills from the job description that are missing in the following resume."""

input_prompt6 = """You are an AI interview coach. Generate potential interview questions that the candidate should prepare for based on the following resume and job description."""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit5:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt5,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")    


elif submit6:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt6,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")   

elif submit7:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt7,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")   

elif submit4:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")


elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
