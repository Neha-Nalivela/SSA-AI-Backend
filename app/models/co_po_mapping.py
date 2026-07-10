from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class COPOMapping(Base):
    __tablename__ = "co_po_mappings"

    id = Column(Integer, primary_key=True, index=True)

    course_outcome_id = Column(
        Integer,
        ForeignKey("course_outcomes.id"),
        nullable=False
    )

    program_outcome_id = Column(
        Integer,
        ForeignKey("program_outcomes.id"),
        nullable=False
    )

    mapping_level = Column(Integer, nullable=False)