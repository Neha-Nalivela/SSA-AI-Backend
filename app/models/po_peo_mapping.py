from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class POPEOMapping(Base):
    __tablename__ = "po_peo_mappings"

    id = Column(Integer, primary_key=True, index=True)

    program_outcome_id = Column(
        Integer,
        ForeignKey("program_outcomes.id"),
        nullable=False
    )

    peo_id = Column(
        Integer,
        ForeignKey("program_educational_objectives.id"),
        nullable=False
    )

    mapping_level = Column(Integer, nullable=False)