# ATS Resume Scanner (Groq AI)

An AI-powered Applicant Tracking System (ATS) Resume Scanner built using **Streamlit**, **Groq LLM**, and **AWS EC2**.  
The application analyzes a resume against a job description to provide ATS insights such as resume evaluation, keyword extraction, and match percentage.

---

## 🚀 Features

- Upload resume in **PDF format**
- Paste **Job Description**
- AI-powered analysis using **Groq LLM**
- Resume evaluation (strengths & weaknesses)
- ATS keyword extraction (JSON output)
- Resume–Job Description match percentage
- Deployed on **AWS EC2**

---

## 🧠 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python  
- **LLM Provider**: Groq  
- **Model Used**: `llama-3.1-8b-instant`  
- **Cloud**: AWS EC2 (Ubuntu 24.04 LTS)  
- **PDF Processing**: pdf2image + poppler  
- **Secrets Management**: Streamlit Secrets  

---

## 🏗️ Architecture Overview

1. User uploads a resume (PDF) and enters a job description
2. Streamlit processes input and extracts resume content
3. Resume + JD are sent to Groq LLM
4. LLM analyzes content and returns ATS insights
5. Results are displayed in the web UI




