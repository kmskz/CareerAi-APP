import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
PROJECT_ID = "textdemo-472317"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load Gemini model
model = GenerativeModel("gemini-2.0-flash")


def analyze_skill_gap(skills: str, target_role: str):
    """
    AI-powered skill gap analysis using Gemini on Vertex AI.
    Returns a Markdown table string.
    """
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    prompt = f"""
    The user has the following skills: {skills_list}.
    The target job role is: {target_role}.

    Provide the missing skills in a **Markdown table** with 2 columns:
    | Missing Skill | Learning Resources |
    Only return the table, no explanations.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error in skill gap analysis: {e}")
        # Fallback markdown table
        return """
        | Missing Skill | Learning Resources |
        |---------------|---------------------|
        | Python        | [Python.org](https://www.python.org/) |
        | SQL           | [W3Schools SQL](https://www.w3schools.com/sql/) |
        | Machine Learning | [Coursera](https://www.coursera.org/) |
        """


