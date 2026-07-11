from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class ProgramObjective(Base):
    __tablename__ = "program_objectives"

    id = Column(Integer, primary_key=True, index=True)

    program_id = Column(
        Integer,
        ForeignKey("programs.id"),
        nullable=False
    )

    objective_code = Column(
        String(20),
        nullable=False,
        unique=True
    )

    description = Column(
        String(500),
        nullable=False
    )