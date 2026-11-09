"""
SQLAlchemy ORM models for the Adapting Student AI Learning and Quiz Agent.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Student(Base):
    """Student/user account model."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    quiz_attempts = relationship("QuizAttempt", back_populates="student", cascade="all, delete-orphan")
    study_schedules = relationship("StudySchedule", back_populates="student", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="student", cascade="all, delete-orphan")
    subjects = relationship("Subject", back_populates="student", cascade="all, delete-orphan")


class Subject(Base):
    """Academic subject belonging to a student (e.g., Data Structures, AI)."""
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), default="")
    semester = Column(Integer, default=1)
    description = Column(Text, default="")

    student = relationship("Student", back_populates="subjects")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")


class Topic(Base):
    """Topic within a subject (e.g., Sorting Algorithms)."""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, default="")
    difficulty = Column(Integer, default=3)  # 1 (easy) to 5 (hard)
    priority = Column(String(20), default="Medium")  # Low, Medium, High

    subject = relationship("Subject", back_populates="topics")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="topic", cascade="all, delete-orphan")


class Question(Base):
    """Multiple-choice question belonging to a topic."""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    text = Column(Text, nullable=False)
    option_a = Column(String(500), nullable=False)
    option_b = Column(String(500), nullable=False)
    option_c = Column(String(500), nullable=False)
    option_d = Column(String(500), nullable=False)
    correct_option = Column(String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    difficulty = Column(Integer, default=3)  # 1-5
    explanation = Column(Text, default="")

    topic = relationship("Topic", back_populates="questions")
    quiz_responses = relationship("QuizResponse", back_populates="question")


class QuizAttempt(Base):
    """Record of a single quiz attempt by a student on a topic."""
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    score = Column(Float, nullable=False)  # Percentage score 0-100
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    student = relationship("Student", back_populates="quiz_attempts")
    topic = relationship("Topic", back_populates="quiz_attempts")
    responses = relationship("QuizResponse", back_populates="attempt", cascade="all, delete-orphan")


class QuizResponse(Base):
    """Individual question response within a quiz attempt."""
    __tablename__ = "quiz_responses"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_option = Column(String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    is_correct = Column(Boolean, nullable=False)

    attempt = relationship("QuizAttempt", back_populates="responses")
    question = relationship("Question", back_populates="quiz_responses")


class StudySchedule(Base):
    """CSP-generated study schedule stored as JSON."""
    __tablename__ = "study_schedules"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    schedule_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    student = relationship("Student", back_populates="study_schedules")


class Recommendation(Base):
    """AI-generated recommendation stored as JSON."""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    recommendations_json = Column(Text, nullable=False)
    engine = Column(String(50), nullable=False)  # 'heuristic', 'fol', 'ml'
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    student = relationship("Student", back_populates="recommendations")
