# Adapting Student AI Learning and Quiz Agent

An intelligent, adaptive learning platform engineered with four distinct core AI methodologies:
1. **Module 2: Heuristic Topic Prioritization (Informed Search)**
2. **Module 3: Constraint Satisfaction Problem (CSP) Study Scheduler**
3. **Module 4: First-Order Logic (FOL) Forward Chaining Inference Engine**
4. **Module 5: Supervised Inductive Learning (Decision Tree Classifier)**

---

## 🌟 Key Features

- **Personalized Adaptive Quizzes:** Automatically assesses past student performance to calibrate question difficulty dynamically (Levels 1–5).
- **Heuristic Focus Ranking:** Evaluates topic weaknesses using an informed evaluation function $h(n)$ with custom multi-factor weights (weakness, error rate, difficulty, revision urgency).
- **Conflict-Free Study Timetable:** Solves a weekly scheduling Constraint Satisfaction Problem using AC-3 arc consistency and Minimum Remaining Values (MRV) backtracking.
- **Declarative Knowledge Base:** Runs forward chaining deduction on Horn clauses to infer tailored remediation recommendations with complete proof traces.
- **Machine Learning Activity Predictor:** Trained Decision Tree Classifier (scikit-learn) predicting optimal next study actions based on live student performance feature vectors.
- **Faculty / Admin Portal:** Manage question banks, calibrate difficulties, and structure subjects and topics.

---

## 🏗️ System Architecture

```
Adapting student ai learning and quiz agent/
├── backend/
│   ├── main.py                    # FastAPI application & SPA static server
│   ├── database.py                # SQLite / SQLAlchemy engine & session
│   ├── models.py                  # ORM database models
│   ├── schemas.py                 # Pydantic validation schemas
│   ├── auth.py                    # JWT authentication & native bcrypt hashing
│   ├── seed_data.py               # Pre-populated curriculum (80 questions, 16 topics)
│   ├── requirements.txt           # Python dependencies
│   ├── ai/
│   │   ├── heuristic.py           # Module 2: Informed heuristic evaluation function
│   │   ├── csp_scheduler.py       # Module 3: AC-3 + MRV backtracking scheduler
│   │   ├── fol_engine.py          # Module 4: Knowledge base & forward chaining engine
│   │   └── decision_tree.py       # Module 5: Scikit-learn decision tree classifier
│   ├── routers/
│   │   ├── auth.py                # Register, login, profile (/api/auth)
│   │   ├── subjects.py            # Subjects & topics listing (/api/subjects)
│   │   ├── quiz.py                # Quiz start, submit, results, history (/api/quiz)
│   │   ├── dashboard.py           # Analytics & scores breakdown (/api/dashboard)
│   │   ├── recommendations.py     # Heuristic priorities & FOL rules (/api/ai)
│   │   ├── schedule.py            # CSP timetable generation (/api/ai)
│   │   ├── predictions.py         # ML activity predictions (/api/ai)
│   │   └── admin.py               # Question bank management (/api/admin)
│   └── tests/                     # 51 unit tests (100% passing)
│       ├── test_heuristic.py
│       ├── test_csp.py
│       ├── test_fol.py
│       └── test_decision_tree.py
├── frontend/
│   ├── src/
│   │   ├── index.css              # Premium glassmorphic modern design system
│   │   ├── api.js                 # API client with JWT interception
│   │   ├── context/AuthContext.jsx# Session and state provider
│   │   ├── components/Navbar.jsx  # Navigation bar with role badges
│   │   └── pages/
│   │       ├── Login.jsx          # 1-click demo login & authentication
│   │       ├── Register.jsx       # Student registration
│   │       ├── Dashboard.jsx      # Progress metrics, weak topics, recent quizzes
│   │       ├── Subjects.jsx       # Curriculum browser & quiz launcher
│   │       ├── Quiz.jsx           # Adaptive quiz interface with question timer
│   │       ├── Results.jsx        # Instant scoring, explanations, confetti
│   │       ├── Recommendations.jsx# Heuristic ranks & FOL derivation trace
│   │       ├── Schedule.jsx       # Interactive CSP weekly study grid
│   │       ├── Predictions.jsx    # Decision tree simulator & feature vectors
│   │       └── Admin.jsx          # Question creation & inventory control
│   └── dist/                      # Production built frontend bundle
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Run the Backend & Web App (Single Command)

From the `backend` directory:
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

### 2. Demo User Accounts

The database comes pre-seeded with curriculum data and demo accounts:

| Role | Email | Password |
|---|---|---|
| **Demo Student** | `student@example.com` | `student123` |
| **Demo Admin** | `admin@example.com` | `admin123` |

*(Fast 1-click login buttons are also available on the Login screen).*

---

## 🧪 Running Automated Tests

All 51 AI algorithm and integration unit tests can be executed via `pytest`:
```bash
cd backend
python -m pytest tests/ -v
```

All 51 tests pass:
- `tests/test_csp.py` (9 tests)
- `tests/test_decision_tree.py` (18 tests)
- `tests/test_fol.py` (14 tests)
- `tests/test_heuristic.py` (10 tests)

---

## 🧠 AI Module Details

### Module 2 — Informed Heuristic Search Evaluation
Guides topic recommendation order using an evaluation metric:
$$\text{Priority}(T) = w_1 \cdot \text{Weakness} + w_2 \cdot \text{Difficulty} + w_3 \cdot \text{RevisionUrgency} + w_4 \cdot \text{ErrorRate}$$

### Module 3 — CSP Study Scheduler
- **Variables:** Available timetable slots `(Day, Hour)`
- **Domains:** Eligible topics
- **Constraints:**
  - Max daily study limit per topic
  - Fatigue avoidance: strictly prohibits identical topics in consecutive time slots
  - Balanced cognitive load: weaker topics receive up to $2\times$ more allocation
  - AC-3 Arc Consistency domain pruning + MRV (Minimum Remaining Values) backtracking

### Module 4 — First-Order Logic (FOL) Inference Engine
Asserts performance facts into working memory:
- $\text{score}(S, T, V)$
- $\text{attempts}(S, T, N)$
- $\text{difficulty}(T, D)$

Applies Horn clause forward chaining until reaching a fixed point:
$$R_4: \text{weak}(S, T) \land \text{difficulty}(T, D) \land D \ge 4 \implies \text{recommend}(S, T, \text{"basic\_revision"})$$
Displays a transparent step-by-step derivation trace.

### Module 5 — Supervised Inductive Learning
- Trains a `DecisionTreeClassifier` on multi-attribute feature vectors: `[avg_score, attempt_count, error_rate, topic_difficulty, days_since_last_attempt]`.
- Predicts activities: `basic_revision`, `concept_review`, `practice_quiz`, `advanced_quiz`.
- Includes an interactive real-time What-If parameter simulator in the frontend.
