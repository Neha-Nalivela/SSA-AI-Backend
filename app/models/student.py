from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    roll_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    gender = Column(String(10))

    year = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    cgpa = Column(DECIMAL(4, 2), default=0.00)
    attendance = Column(DECIMAL(5, 2), default=0.00)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )
    department = relationship("Department")
    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )