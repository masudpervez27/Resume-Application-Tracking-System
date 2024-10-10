from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os 
import base64
import io
from PIL import Image
from PyPDF2 import PdfFileReader
import pdf2image
import google.generativeai as genai
# import vertexai
# from vertexai.preview.generative_models import GenerativeModel

# project_id = ""
# location = ""

# vertexai.init(project=project_id, location=location)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(upload_file):

    if upload_file is not None:
        ## convert pdf to image
        image = pdf2image.convert_from_bytes(upload_file.read())

        first_page = image[0]
        # convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() # encode to base64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


## Stramlit APP

from streamlit_pdf_viewer import pdf_viewer

container_pdf, container_chat = st.columns([50, 50])

# st.set_page_config(page_title="ATS Resume Expert")
# Description
st.write("""
This app allows you to upload a file. You can upload various file types like PDFs, images, or text files.
After uploading, it will display the file details for you to inspect.
""")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description: ", key="input")

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF) ...", type=["pdf"])

# Displaying the uploaded file's details
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

    # Display file type
    file_details = {
        "Filename": uploaded_file.name,
        "FileType": uploaded_file.type,
        "FileSize": uploaded_file.size
    }

    st.write("File Details:")
    st.json(file_details)

    # Displaying PDF content or image

    if uploaded_file.type == "application/pdf":
        # Display the PDF content
        st.header("PDF Content")
        binary_data = uploaded_file.getvalue()
        pdf_viewer(input=binary_data, width=700)

    elif uploaded_file.type.startswith("image"):
        # Display the image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    elif uploaded_file.type == "text/plain":
        # Display text content
        text = uploaded_file.read().decode("utf-8")
        st.text_area("Text Content", text)

    else:
        st.write("Unsupported file type.")
else:
    st.write("Please upload a file to proceed.")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How can I Improve my Skills")

# submit3 = st.button("What are the Keywords That are Missing")

submit4 = st.button("Percentage match")


input_prompt1 = """
You are an experienced HR with Technical Experience in the field of Data Science, Full stack Web Development, Big Data Engineering, DevOps, Data Analyst,
your task is to review the provided resume against the job description for this specific profile.
Please share your professional evaluation on whether the candidate's profile aligns with the role. Highlight the strength and weaknesses of the applicant
in relation to the specified job requirement.
"""

input_prompt2 = """
You are an experienced HR with Technical Experience in the field of Data Science, Full stack Web Development, Big Data Engineering, DevOps, Data Analyst,
your role is to scrutinize the resume in the  light of the job description provided.
Share your insights on the candidate's suitability for the role from an HR perspective. Additionally, offer advice on enhancing the candidate's skills and
identify areas to improve.
"""

input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full stack Web Development, Big Data Engineering, DevOps, Data Analyst
and deep ATS functionality.
Evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description.
First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        # st.write(response)
    else:
        st.write("Please upload an resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        # st.write(response)
    else:
        st.write("Please upload an resume")

# if __name__ == "__main__":
#     get_response("Explain how AI works")