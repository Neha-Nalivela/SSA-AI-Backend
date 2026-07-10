from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, DECIMAL
from sqlalchemy.sql import func

from app.database import Base


class QuestionCOMap(Base):
    __tablename__ = "question_co_mappings"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    course_outcome_id = Column(
        Integer,
        ForeignKey("course_outcomes.id"),
        nullable=False
    )

    weightage = Column(
        DECIMAL(5, 2),
        default=100.00
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )