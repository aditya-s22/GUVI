'''from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

sessions = {}

class StartRequest(BaseModel):
    role: str
    mode: str
    num_questions: int = 4

class AnswerRequest(BaseModel):
    session_id: str
    question_idx: int
    answer: str

@app.post("/start")
def start_interview(req: StartRequest):
    session_id = str(uuid.uuid4())
    questions = [{"title": f"{req.mode.title()} Q{i+1}", "desc": f"Sample {req.mode} question {i+1}"} for i in range(req.num_questions)]
    sessions[session_id] = {"role": req.role, "mode": req.mode, "questions": questions, "answers": []}
    return {"session_id": session_id, "questions": questions}

@app.post("/answer")
def answer_question(req: AnswerRequest):
    session = sessions.get(req.session_id)
    if not session:
        return {"error": "Session not found"}
    question = session["questions"][req.question_idx]
    evaluation = {"clarity": "Good", "completeness": "Satisfactory", "suggestions": "Keep practicing!"}
    session["answers"].append({"question": question, "answer": req.answer, "evaluation": evaluation})
    return {"evaluation": evaluation}
'''
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/answer")
def answer_question(req: AnswerRequest):
    session = sessions.get(req.session_id)
    if not session:
        return {"error": "Session not found"}
    question = session["questions"][req.question_idx]
    
    # Use GPT to evaluate the answer
    prompt = f"Evaluate the following answer to the question:\n\nQ: {question['desc']}\nA: {req.answer}\n\nGive clarity, completeness, and suggestions in JSON."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    evaluation_text = response['choices'][0]['message']['content']
    
    # Optional: Try to parse it as JSON
    import json
    try:
        evaluation = json.loads(evaluation_text)
    except:
        evaluation = {"clarity": "Good", "completeness": "Satisfactory", "suggestions": evaluation_text}

    session["answers"].append({"question": question, "answer": req.answer, "evaluation": evaluation})
    return {"evaluation": evaluation}
