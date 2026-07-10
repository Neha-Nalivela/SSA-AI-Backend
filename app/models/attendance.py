from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )

    total_classes = Column(Integer, nullable=False)

    attended_classes = Column(Integer, nullable=False)

    attendance_percentage = Column(Float, nullable=False)

    semester = Column(String(20), nullable=False)

    academic_year = Column(String(20), nullable=False)