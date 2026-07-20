from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func

from app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    question_number = Column(String(10), nullable=False)

    question_text = Column(String(500), nullable=False)

    max_marks = Column(Integer, nullable=False)

    assessment_id = Column(
        Integer,
        ForeignKey("assessments.id"),
        nullable=False
    )

    # -------------------------
    # NEW FIELDS
    # -------------------------

    co = Column(
        String(10),
        nullable=True
    )

    btl = Column(
        String(20),
        nullable=True
    )

    # -------------------------

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )