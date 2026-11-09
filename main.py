"""
FastAPI application entry point.
Registers all routers and initializes the database.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from models import Student, Subject, Topic, Question, QuizAttempt, QuizResponse, StudySchedule, Recommendation
from seed_data import seed_database
from ai.decision_tree import ActivityPredictor

from routers import auth, subjects, quiz, dashboard, recommendations, schedule, predictions, admin

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Adapting Student AI Learning and Quiz Agent",
    description="An AI-powered adaptive learning platform that analyzes student quiz performance, "
                "identifies weak topics, generates personalized study schedules, and predicts learning activities.",
    version="1.0.0",
)

# CORS middleware for frontend (supports local dev and Netlify deployments)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(subjects.router)
app.include_router(subjects.topics_router)
app.include_router(quiz.router)
app.include_router(dashboard.router)
app.include_router(recommendations.router)
app.include_router(schedule.router)
app.include_router(predictions.router)
app.include_router(admin.router)


@app.on_event("startup")
def startup_event():
    """Seed database and train ML model on startup."""
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    # Pre-train the decision tree model
    print("[*] Training Decision Tree model...")
    predictor = ActivityPredictor()
    metrics = predictor.train()
    print(f"   Model accuracy: {metrics['accuracy']:.2%}")


@app.get("/api/health")
def health():
    return {"status": "healthy"}


import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not Found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "app": "Adapting Student AI Learning and Quiz Agent",
            "version": "1.0.0",
            "docs": "/docs",
            "ai_modules": [
                "Module 2: Heuristic Topic Prioritization",
                "Module 3: CSP Study Scheduler",
                "Module 4: FOL Forward Chaining",
                "Module 5: Decision Tree Classifier",
            ],
        }
