from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class CourseObjective(Base):
    __tablename__ = "course_objectives"

    id = Column(Integer, primary_key=True, index=True)

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )

    objective_code = Column(String(20), nullable=False)

    description = Column(String(500), nullable=False)