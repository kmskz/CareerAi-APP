# utils/parse_resume.py
from google.cloud import documentai_v1 as documentai
import re

PROJECT_ID = "201142552428"
LOCATION = "us"  # must match your Form Parser processor
PROCESSOR_ID = "c90a8a108be2fa5f"

def extract_resume_fields(text):
    """Very basic regex-based resume parsing."""
    data = {}

    # Name: assume first non-empty line
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if lines:
        data["name"] = lines[0]

    # Email
    email = re.search(r"[\w\.-]+@[\w\.-]+", text)
    if email:
        data["email"] = email.group(0)

    # Phone
    phone = re.search(r"\+?\d[\d\s\-\(\)]+", text)
    if phone:
        data["phone"] = phone.group(0)

    # LinkedIn
    linkedin = re.search(r"(linkedin\.com\/[^\s]+)", text, re.IGNORECASE)
    if linkedin:
        data["linkedin"] = linkedin.group(0)

    # Education (very simple keyword search)
    education = []
    for line in lines:
        if "University" in line or "College" in line or "Bachelor" in line or "Master" in line:
            education.append(line)
    if education:
        data["education"] = education

    # Skills: look for a "Skills" section
    skills = []
    capture = False
    for line in lines:
        if "skills" in line.lower():
            capture = True
            continue
        if capture:
            if line.strip() == "" or any(x in line.lower() for x in ["experience", "education", "summary"]):
                break
            skills.extend([s.strip() for s in re.split(r",|;|\|", line) if s.strip()])
    if skills:
        data["skills"] = skills

    return data


def parse_resume(file):
    """Parse resume with Document AI Form Parser + regex post-processing."""
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    # Read file
    content = file.getvalue()
    raw_document = documentai.RawDocument(
        content=content,
        mime_type=file.type
    )

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
    )

    try:
        result = client.process_document(request=request)
    except Exception as e:
        return {"error": str(e)}

    document = result.document
    text = document.text or ""

    # Extract structured fields manually
    fields = extract_resume_fields(text)

    return {
        "text_preview": text[:500] + "...",
        "entities": fields
    }










