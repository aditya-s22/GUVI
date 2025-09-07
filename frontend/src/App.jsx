import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000"; // Backend URL

function App() {
  const [role, setRole] = useState("Software Engineer");
  const [mode, setMode] = useState("technical");
  const [session, setSession] = useState(null);
  const [current, setCurrent] = useState(0);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState(null);

  const startInterview = async () => {
    try {
      const res = await axios.post(`${API_BASE}/start`, { role, mode, num_questions: 4 });
      setSession(res.data);
      setCurrent(0);
      setAnswer("");
      setFeedback(null);
    } catch (err) {
      alert("Failed to start session: " + (err?.response?.data?.detail || err.message));
    }
  };

  const submitAnswer = async () => {
    if (!session) return;
    try {
      const payload = { session_id: session.session_id, question_idx: current, answer };
      const res = await axios.post(`${API_BASE}/answer`, payload);
      setFeedback(res.data.evaluation);
    } catch (err) {
      alert("Failed to submit answer: " + (err?.response?.data?.detail || err.message));
    }
  };

  const nextQuestion = () => {
    if (!session) return;
    setCurrent((i) => Math.min(i + 1, session.questions.length - 1));
    setAnswer("");
    setFeedback(null);
  };

  const prevQuestion = () => {
    if (!session) return;
    setCurrent((i) => Math.max(i - 1, 0));
    setAnswer("");
    setFeedback(null);
  };

  return (
    <div className="container">
      <h1>InterviewBot — Mock Interview</h1>

      {!session && (
        <div>
          <label>Role:</label>
          <input value={role} onChange={(e) => setRole(e.target.value)} />
          <br />
          <label>Mode:</label>
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="technical">Technical</option>
            <option value="behavioral">Behavioral</option>
          </select>
          <br />
          <button className="primary" onClick={startInterview}>Start Interview</button>
        </div>
      )}

      {session && (
        <div>
          <h2>Question {current + 1} / {session.questions.length}</h2>
          <p>{session.questions[current]?.desc || session.questions[current]?.title}</p>

          <textarea value={answer} onChange={(e) => setAnswer(e.target.value)} rows={6} placeholder="Type your answer here..." />

          <div>
            <button className="success" onClick={submitAnswer}>Submit</button>
            <button className="gray" onClick={() => { setAnswer(""); setFeedback(null); }}>Retry</button>
            <button className="primary" onClick={nextQuestion}>Next</button>
            <button className="gray" onClick={prevQuestion}>Prev</button>
          </div>

          {feedback && (
            <div style={{marginTop: "10px", padding: "10px", backgroundColor: "#eee", borderRadius: "4px"}}>
              <strong>Feedback:</strong>
              <pre>{JSON.stringify(feedback, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
