from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)

    subject_code = Column(String(20), unique=True, nullable=False)
    subject_name = Column(String(100), nullable=False)

    credits = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    faculty_id = Column(
        Integer,
        ForeignKey("faculties.id"),
        nullable=False
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )