from fastapi import FastAPI, UploadFile, Form
from nlp_utils import extract_skills
from interview_engine import InterviewEngine
from pypdf import PdfReader
from io import BytesIO

app = FastAPI()
engine = None

def read_pdf(upload_file: UploadFile):
    pdf_bytes = upload_file.file.read()
    reader = PdfReader(BytesIO(pdf_bytes))

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text

@app.post("/start_interview/")
async def start_interview(resume: UploadFile, jd: str = Form(...)):
    global engine

    resume_text = read_pdf(resume)
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd)

    overlap = list(set(resume_skills) & set(jd_skills))
    engine = InterviewEngine(overlap)

    question, time_limit = engine.get_question()

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "question": question,
        "time_limit": time_limit
    }

@app.post("/answer/")
async def answer(answer: str = Form(...), time_taken: int = Form(...)):
    global engine

    score = engine.evaluate(answer, time_taken)

    if engine.terminated:
        return {"message": "Interview terminated early", "final_score": engine.final_score()}

    question, time_limit = engine.get_question()

    return {
        "score": score,
        "next_question": question,
        "time_limit": time_limit
    }

@app.get("/result/")
def result():
    return {"final_readiness_score": engine.final_score()}

