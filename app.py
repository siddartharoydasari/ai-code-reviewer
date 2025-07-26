import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env file or environment variable
load_dotenv()
GEMINI_API_KEY =("ENTER API KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Supported languages (you can add more as needed)
SUPPORTED_LANGUAGES = ["Python", "Java", "JavaScript", "C++", "Go"]

# Prompt template for reviewing code
REVIEW_PROMPT = """
You are an experienced software engineer. Review the following {language} code for:
- Code quality
- Potential bugs
- Security issues
- Best practices
- Suggestions for improvement

Return the review in markdown format with headers and bullet points.

Code:
```
{code}
```
"""

st.set_page_config(page_title="AI Code Reviewer Bot", layout="wide")
st.title("🤖 AI Code Reviewer Bot")

st.markdown("""Upload or paste your code and get a smart review powered by Gemini Pro.
Supports multiple languages including Python, Java, and more.
""")

# Input method
code_input_method = st.radio("Choose input method:", ["Paste code", "Upload file"])

code = ""
if code_input_method == "Paste code":
    code = st.text_area("Paste your code here:", height=300)
else:
    uploaded_file = st.file_uploader("Upload your code file:", type=["py", "java", "js", "cpp", "go"])
    if uploaded_file:
        code = uploaded_file.read().decode("utf-8")

language = st.selectbox("Select the programming language:", SUPPORTED_LANGUAGES)

if st.button("🔍 Review Code"):
    if not code.strip():
        st.warning("Please provide code for review.")
    else:
        with st.spinner("Reviewing your code with Gemini..."):
            prompt = REVIEW_PROMPT.format(language=language, code=code)
            try:
                response = model.generate_content(prompt)
                st.markdown("### 📝 Gemini's Code Review")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error during Gemini API call: {e}")
