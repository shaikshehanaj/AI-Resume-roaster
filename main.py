import streamlit as st
from dotenv import load_dotenv
import io 
import os
import PyPDF2
import google.generativeai as genai




import streamlit as st
from dotenv import load_dotenv
import io, os
import PyPDF2
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("💥 GEMINI_API_KEY not found in environment variables"); st.stop()

genai.configure(api_key=API_KEY)

st.title('AI Resume roaster')
st.badge('chai aur code')
st.markdown('Upload your resume and get AI powered roasting')
st.divider()

uploaded_file = st.file_uploader('Upload your resume here (PDF and text only)',type=['pdf','txt'])
job_role = st.text_input('Enter the job role that you are targeting')
# options = ['Software Engineering','Accounts & Finance','Customer Service','Bank jobs']
# selection = st.pills('Job_roles', options, selection_mode = 'multi')

# st.markdown(f'Your selection options: {selection}.')
analyze = st.button('Analyze resume')
print(analyze)

def extract_text_from_pdf(file_bytes):
    reader = PyPDF2.PdfReader(file_bytes)
    return '\n'.join(page.extract_text() or '' for page in reader.pages)

def extract_text(uploaded_file):
    """Extracts text from an uploaded pdf or text"""
    file_type = uploaded_file.type

    if file_type == 'application/pdf':
        with io.BytesIO(uploaded_file.read()) as file_bytes:
            return extract_text_from_pdf(file_bytes)
    elif file_type == 'text/plain':
        return uploaded_file.read().decode('utf-8')
    else:
        return ""

if analyze and uploaded_file:
    try :
        file_content = extract_text(uploaded_file)

        if not file_content.strip():
            st.error('File does not have any content')
            st.stop()

        prompt = f''' 
You are brutally honest, no non-sense HR expert who's been reviewig resumes for decades 
Roast this resume like you are on a comedy stage but still give some useful insights feedback.
Don't hold back - be sarcastic, witty and critical where needed. 
Would make this resume actually land a job in {job_role} for a good company.
here is the resume, go wild:
{file_content}  

Make it sting and make sure to keep it in 150 words. Answer everything in Hinglish.

'''

        #AI Calling
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.markdown('## Analyze Results')
        st.markdown(response.text)

    except Exception as e:
        st.error(f'An error occured: {e}')