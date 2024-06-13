import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

## Prompt Template for Resume Builder
resume_input_prompt = """
Hey Act Like a skilled or very experienced Resume Builder
with a deep understanding of how to make the best professional resumes.
Your task includes: 
1) Get the job role the user is preparing for.
2) Convert the experience entered by the user in casual language to professional bullet points to be inserted in the What were your responsibilities and accomplishments? in the experience section of the resume .
3) Convert the role in the project entered by the user in casual language into professional bullet points to be inserted in the project decription section in the resume.
4) From the experience and the projects done, Generate a list of skills that the user has and the list of skills that is required for the job role.
5) Based on the experience and projects done, Generate a brief professional summary of the user that needs to be added in the resume.
You must consider the job market is very competitive and you should provide best assistance for improving the resumes.

Here are some helpful tips to help you build and review your resume.
Maximize first impressions
On average, recruiters spend less than 10 seconds reviewing a resume, so be concise. Pertinent info should be on the first page as the recruiter may not read beyond that.
Resume formatting tips
Format for consistency. Spacing, punctuation, font, bullet points, and tense should be consistent.
Format resume sections in the following order: Header, Professional Summary, Skills, Professional Experience, and Education with additional sections as needed.
These days, a 2-page resume is most common. If you are fresh out of college or only have a few years of experience, you shouldn't have to go over 1 page. But once you have around 5+ years, you can go to 2 pages, which should help if you find it difficult to fit your entire work history to 1 page. The only situations where you would go to 3 pages or more would be at the Chief Executive level, an academic CV, or a federal resume that requires a very specific format.
Power up your language
Vary up the verbs you use at the beginning of bullet points. Instead of always saying "Led" or "managed", try mixing it up with "spearheaded," "headed," "guided," "directed," "steered," etc.
Try to avoid overused and lukewarm words and phrases like "responsible for," "managed," and "handled." Always try to use stronger verbs that position you as an achiever and someone who takes initiative rather than just a doer or someone who is passive.
Leave out skills and responsibilities that aren't relevant to the role you're applying for, especially if they are things you don't enjoy doing and don't want to do in your next role.
What needs to avoid
Don't include reasons for leaving your past jobs. If there is a large gap in your work history or something else that might be glaring, you can address it in your cover letter.
Don't include salary information on your resume.
Don't list your references on your resume. You don't want your references to have to take calls/emails without preparation. Once you are far along enough in the interview process, they will ask for your references and you can provide them at that time. Contact your references, let them know about the position you're interviewing for, and give them some talking points to highlight that will be most relevant to the job. Also omit "References Available Upon Request". That's a given, and it just takes up space on your resume that you could devote to something more important.

Generate the resume for these conditions:
Job Role:{role}
Experience:{xp}
Project Role:{pr}

I want the response in this structure


The Job your applying for is .

Your Experience is.

Your Projects are.

The Skills you have and the skills you require are.

This is the Summary of your resume.
"""

## Prompt Template for ATS
ats_input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst and big data engineer. Your task is to evaluate the resume based on the given job description and skills.
Use the url to analyze the company and extract the company details , skills and job description.
You must consider the job market is very competitive and you should provide best assistance for improving the resumes. Assign the percentage Matching based on Jd and 
the missing keywords with high accuracy
resume:{text}
description:{jd}
skills:{sk}
I want the response having the structure

{{"JD Match": "%","Skill Match" : "%", MissingKeywords:[]","Profile Summary":""}}


What are the chances of me getting the Job?

What are the skills I need?

How much experience is needed?


"""

# Sidebar with dropdown menu
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose the app", ["Resume Builder", "ATS"])

if app_mode == "Resume Builder":
    st.title("Resume Builder")
    st.text("Build Your Resume. Find out what are the skills you are lacking")

    role = st.text_area("Enter job role you are applying for.")
    xp = st.text_area("Enter your experience at your current/previous job roles. Mention Company Name, Role and what you were working on.")
    pr = st.text_area("Enter your projects here. Mention Project Name, Project Description and your role in the Project ")

    submit = st.button("Submit")

    if submit:
        prompt = resume_input_prompt.format(role=role, xp=xp, pr=pr)
        response = get_gemini_response(prompt)
        st.subheader(response)

elif app_mode == "ATS":
    st.title("Smart ATS")
    st.text("Improve Your Resume ATS")

    jd = st.text_area("Add Job Description")
    sk = st.text_area("Add Skills")
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

    submit = st.button("Submit")

    if submit:
        if uploaded_file is not None:
            text = input_pdf_text(uploaded_file)
            prompt = ats_input_prompt.format(text=text, jd=jd, sk=sk)
            response = get_gemini_response(prompt)
            st.subheader(response)
