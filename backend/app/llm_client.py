import os, json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_llm(prompt: str) -> dict:
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an interview generator."},
                  {"role": "user", "content": prompt}],
        max_tokens=500,
    )
    text = resp.choices[0].message["content"]
    try:
        return json.loads(text)
    except:
        return {"questions": [{"title": "Error parsing response", "desc": text}]}

async def evaluate_answer(prompt: str) -> dict:
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an interview evaluator."},
                  {"role": "user", "content": prompt}],
        max_tokens=500,
    )
    text = resp.choices[0].message["content"]
    try:
        return json.loads(text)
    except:
        return {"feedback": text}
