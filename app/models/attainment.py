from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Attainment(Base):
    __tablename__ = "attainments"

    id = Column(Integer, primary_key=True, index=True)

    course_outcome_id = Column(
        Integer,
        ForeignKey("course_outcomes.id"),
        nullable=False
    )

    program_outcome_id = Column(
        Integer,
        ForeignKey("program_outcomes.id"),
        nullable=True
    )

    attainment_percentage = Column(Float, nullable=False)

    semester = Column(String(20), nullable=False)

    academic_year = Column(String(20), nullable=False)

    calculated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )