import streamlit as st
import pdf2image
import json
from groq import Groq

# -------------------------------------------------
# Groq Configuration
# -------------------------------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

MODEL_NAME = "llama-3.1-8b-instant"

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------

@st.cache_data(show_spinner="Extracting resume text...")
def extract_text_from_pdf(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    text = ""
    for img in images:
        text += str(img) + "\n"
    return text


@st.cache_data(show_spinner="Analyzing with ATS engine...")
def get_llm_response(prompt, resume_text, job_description):
    final_prompt = f"""
{prompt}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an expert ATS resume evaluator."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content


@st.cache_data(show_spinner="Extracting keywords...")
def get_llm_response_keywords(prompt, resume_text, job_description):
    final_prompt = f"""
{prompt}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON.
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an ATS keyword extraction engine."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.1
    )

    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {
            "Technical Skills": [],
            "Analytical Skills": [],
            "Soft Skills": []
        }

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------

st.set_page_config(page_title="ATS Resume Scanner")
st.title("ATS Resume Scanner (Groq AI)")

job_description = st.text_area("Job Description")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if uploaded_file:
    st.success("PDF Uploaded Successfully")
    st.session_state.resume_text = extract_text_from_pdf(uploaded_file)

col1, col2, col3 = st.columns(3)

with col1:
    submit1 = st.button("Tell Me About the Resume")

with col2:
    submit2 = st.button("Get Keywords")

with col3:
    submit3 = st.button("Percentage Match")

# -------------------------------------------------
# Prompts
# -------------------------------------------------

PROMPT_REVIEW = """
You are a Technical Human Resource Manager.
Review the resume against the job description.
Highlight strengths and weaknesses.
"""

PROMPT_KEYWORDS = """
You are an ATS scanner.
Extract required skills strictly from the job description.
Respond ONLY in JSON format:
{
  "Technical Skills": [],
  "Analytical Skills": [],
  "Soft Skills": []
}
"""

PROMPT_PERCENTAGE = """
You are an ATS system.
Evaluate resume vs job description.
Return:
1. Match percentage
2. Missing keywords
3. Final thoughts
"""

# -------------------------------------------------
# Button Logic
# -------------------------------------------------

if submit1:
    if st.session_state.resume_text:
        result = get_llm_response(
            PROMPT_REVIEW,
            st.session_state.resume_text,
            job_description
        )
        st.subheader("Resume Evaluation")
        st.write(result)
    else:
        st.warning("Please upload the resume")

elif submit2:
    if st.session_state.resume_text:
        result = get_llm_response_keywords(
            PROMPT_KEYWORDS,
            st.session_state.resume_text,
            job_description
        )
        st.subheader("Extracted Skills")
        st.write(f"**Technical Skills:** {', '.join(result['Technical Skills'])}")
        st.write(f"**Analytical Skills:** {', '.join(result['Analytical Skills'])}")
        st.write(f"**Soft Skills:** {', '.join(result['Soft Skills'])}")
    else:
        st.warning("Please upload the resume")

elif submit3:
    if st.session_state.resume_text:
        result = get_llm_response(
            PROMPT_PERCENTAGE,
            st.session_state.resume_text,
            job_description
        )
        st.subheader("ATS Match Result")
        st.write(result)
    else:
        st.warning("Please upload the resume")
