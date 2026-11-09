"""
Pydantic schemas for request validation and response serialization.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=150)
    password: str = Field(..., min_length=6)

class StudentLogin(BaseModel):
    email: str
    password: str

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    student: StudentResponse


# ── Subjects & Topics ─────────────────────────────────────────────────

class SubjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: Optional[str] = ""
    semester: Optional[int] = 1
    description: Optional[str] = ""

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    semester: Optional[int] = None
    description: Optional[str] = None

class TopicCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = ""
    difficulty: Optional[int] = 3
    priority: Optional[str] = "Medium"

class TopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[int] = None
    priority: Optional[str] = None

class TopicResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    difficulty: int
    priority: Optional[str] = "Medium"
    subject_id: int
    question_count: Optional[int] = 0
    avg_score: Optional[float] = None
    quizzes_completed: Optional[int] = 0

    class Config:
        from_attributes = True

class SubjectResponse(BaseModel):
    id: int
    student_id: Optional[int] = None
    name: str
    code: Optional[str] = ""
    semester: Optional[int] = 1
    description: Optional[str] = ""
    topics: List[TopicResponse] = []
    total_topics: Optional[int] = 0
    total_quizzes: Optional[int] = 0
    average_score: Optional[float] = 0.0

    class Config:
        from_attributes = True


# ── Questions ─────────────────────────────────────────────────────────

class QuestionCreate(BaseModel):
    topic_id: int
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str = Field(..., pattern="^[ABCDabcd]$")
    difficulty: int = Field(3, ge=1, le=5)

class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_option: Optional[str] = None
    difficulty: Optional[int] = None

class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: int
    # Note: correct_option is NOT sent to students during quiz

    class Config:
        from_attributes = True

class QuestionAdminResponse(QuestionResponse):
    """Includes correct answer — admin only."""
    correct_option: str


# ── Quiz ──────────────────────────────────────────────────────────────

class QuizGenerateRequest(BaseModel):
    subject_id: Optional[int] = None
    topic_id: int
    difficulty: str = Field("Medium", description="Easy, Medium, or Hard")
    num_questions: int = Field(5, ge=1, le=20)

class QuizStartRequest(BaseModel):
    topic_id: Optional[int] = None
    subject_id: Optional[int] = None
    num_questions: int = Field(5, ge=1, le=20)
    difficulty: Optional[str] = Field("Medium", description="Easy, Medium, or Hard")

class QuizQuestionOut(BaseModel):
    id: int
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: int
    subject_name: Optional[str] = None
    topic_name: Optional[str] = None

class QuizStartResponse(BaseModel):
    quiz_session_id: str
    topic_id: Optional[int] = None
    topic_name: str
    subject_name: Optional[str] = None
    difficulty: Optional[str] = "Medium"
    source: Optional[str] = "openai"
    notice: Optional[str] = None
    questions: List[QuizQuestionOut]

class AnswerSubmission(BaseModel):
    question_id: int
    selected_option: str = Field(..., pattern="^[ABCDabcd]$")

class QuizSubmitRequest(BaseModel):
    topic_id: Optional[int] = None
    subject_id: Optional[int] = None
    answers: List[AnswerSubmission]

class QuizResultResponse(BaseModel):
    attempt_id: int
    topic_name: str
    subject_name: Optional[str] = None
    difficulty: Optional[str] = "Medium"
    score: float
    total_questions: int
    correct_answers: int
    incorrect_answers: Optional[int] = 0
    details: List[Dict[str, Any]]

class QuizAttemptSummary(BaseModel):
    id: int
    topic_id: int
    topic_name: str
    subject_name: str
    score: float
    total_questions: int
    correct_answers: int
    created_at: datetime

    class Config:
        from_attributes = True



# ── Dashboard ─────────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_subjects: int = 0
    total_topics: int = 0
    total_quizzes: int = 0
    average_score: float = 0.0
    topics_attempted: int = 0
    best_topic: Optional[str] = None
    weakest_topic: Optional[str] = None
    recent_trend: str = "stable"
    study_streak_days: int = 1

class TopicScoreBreakdown(BaseModel):
    topic_id: int
    topic_name: str
    subject_name: str
    avg_score: float
    attempts: int
    best_score: float
    latest_score: float
    difficulty: int

class ProgressPoint(BaseModel):
    date: str
    score: float
    topic_name: str


# ── AI: Heuristic ────────────────────────────────────────────────────

class TopicPriorityResponse(BaseModel):
    topic_id: int
    topic_name: str
    priority_score: float
    weakness_score: float
    difficulty_score: float
    urgency_score: float
    error_rate_score: float
    recommendation: str


# ── AI: FOL Recommendations ──────────────────────────────────────────

class FOLRecommendation(BaseModel):
    topic_name: str
    activity: str
    derived_by_rule: str
    explanation: str

class FOLResponse(BaseModel):
    recommendations: List[FOLRecommendation]
    derivation_trace: List[Dict[str, Any]]
    total_facts_derived: int


# ── AI: CSP Schedule ─────────────────────────────────────────────────

class ScheduleRequest(BaseModel):
    study_hours_per_day: Optional[List[int]] = None
    daily_study_hours: Optional[int] = Field(3, ge=1, le=8)
    start_time: Optional[str] = Field("09:00 AM")
    session_duration: Optional[int] = Field(45, ge=30, le=120)
    available_days: Optional[List[str]] = None
    max_hours_per_day: Optional[int] = Field(3, ge=1, le=8)
    max_consecutive_hours: Optional[int] = Field(2, ge=1, le=4)
    total_weekly_hours: Optional[int] = Field(15, ge=3, le=40)
    subject_ids: Optional[List[int]] = None
    topic_ids: Optional[List[int]] = None
    exam_date: Optional[str] = None

class ScheduleSlotOut(BaseModel):
    id: Optional[str] = None
    hour: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[str] = "45 mins"
    subject: Optional[str] = "General"
    subject_id: Optional[int] = None
    topic: str
    topic_id: Optional[int] = None
    activity: Optional[str] = "Concept Revision"
    priority: Optional[str] = "Medium"
    is_completed: Optional[bool] = False
    reason: Optional[str] = ""

class ScheduleResponse(BaseModel):
    schedule_id: Optional[int] = None
    schedule: Dict[str, List[ScheduleSlotOut]]
    total_study_hours: int
    topic_distribution: Dict[str, int]
    subject_distribution: Optional[Dict[str, int]] = {}

class SessionUpdateRequest(BaseModel):
    session_id: str
    day: str
    topic: Optional[str] = None
    topic_id: Optional[int] = None
    subject: Optional[str] = None
    subject_id: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    activity: Optional[str] = None
    priority: Optional[str] = None
    is_completed: Optional[bool] = None



# ── AI: ML Predictions ──────────────────────────────────────────────

class PredictionResult(BaseModel):
    topic_id: int
    topic_name: str
    predicted_activity: str
    confidence: float
    probabilities: Dict[str, float]
    features_used: Dict[str, Any]

class PredictionResponse(BaseModel):
    predictions: List[PredictionResult]
    model_accuracy: Optional[float]



