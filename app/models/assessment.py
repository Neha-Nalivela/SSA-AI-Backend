from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    assessment_name = Column(String(100), nullable=False)
    assessment_type = Column(String(50), nullable=False)

    max_marks = Column(Integer, nullable=False)

    exam_date = Column(Date, nullable=False)

    academic_year = Column(String(20), nullable=False)

    semester = Column(Integer, nullable=False)

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )