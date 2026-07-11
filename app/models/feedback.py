from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)

    semester = Column(String(20), nullable=False)
    academic_year = Column(String(20), nullable=False)

    teaching_rating = Column(Float, nullable=False)
    clarity_rating = Column(Float, nullable=False)
    interaction_rating = Column(Float, nullable=False)
    practical_rating = Column(Float, nullable=False)
    assessment_rating = Column(Float, nullable=False)

    difficult_topic = Column(Text)
    suggestions = Column(Text)

    completion_time = Column(Integer)      # seconds
    reliability_score = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())