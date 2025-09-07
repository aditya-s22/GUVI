QUESTION_PROMPT = """
Generate {num} interview questions for a {role} in {domain} domain. Mode: {mode}.
Output JSON like:
{"questions": [{"title": "...", "desc": "..."}]}
"""

EVAL_PROMPT = """
Evaluate the answer to this question. Return JSON:
{"score": 0-10, "strengths": [], "weaknesses": [], "suggestions": [], "feedback": "..."}
Question: {question}
Answer: {answer}
"""

def build_question_prompt(role, domain, mode, num):
    return QUESTION_PROMPT.format(role=role, domain=domain or "general", mode=mode, num=num)

def build_evaluation_prompt(question, answer, mode):
    return EVAL_PROMPT.format(question=question, answer=answer)
