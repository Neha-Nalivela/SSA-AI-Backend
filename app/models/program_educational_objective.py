from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class ProgramEducationalObjective(Base):
    __tablename__ = "program_educational_objectives"

    id = Column(Integer, primary_key=True, index=True)
    peo_code = Column(String(10), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))

    program_id = Column(
        Integer,
        ForeignKey("programs.id"),
        nullable=False
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )