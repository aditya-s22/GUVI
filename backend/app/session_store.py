import uuid

class Session:
    def __init__(self, role, domain, mode, num):
        self.session_id = str(uuid.uuid4())
        self.role = role
        self.domain = domain
        self.mode = mode
        self.num = num
        self.questions = []
        self.answers = {}

    def record_answer(self, idx, answer, evaluation):
        self.answers[idx] = {"answer": answer, "evaluation": evaluation}

    def summary(self):
        scores = [v["evaluation"].get("score", 0) for v in self.answers.values()]
        avg_score = sum(scores)/len(scores) if scores else 0
        return {"avg_score": avg_score, "answers": self.answers, "questions": self.questions}

class InMemorySessionStore:
    def __init__(self): self._store = {}
    def create(self, role, domain, mode, num):
        s = Session(role, domain, mode, num)
        self._store[s.session_id] = s
        return s
    def get(self, session_id): return self._store.get(session_id)
