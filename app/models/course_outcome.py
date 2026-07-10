from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class CourseOutcome(Base):
    __tablename__ = "course_outcomes"

    id = Column(Integer, primary_key=True, index=True)

    co_code = Column(String(10), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))

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