from sqlalchemy.orm import Session

from app.models.attainment import Attainment
from app.models.po_peo_mapping import POPEOMapping


class PEOAttainmentService:

    @staticmethod
    def calculate(
        db: Session,
        peo_id: int,
        semester: str,
        academic_year: str,
    ):
        records = (
            db.query(
                Attainment.attainment_percentage,
                POPEOMapping.mapping_level,
            )
            .join(
                POPEOMapping,
                Attainment.program_outcome_id ==
                POPEOMapping.program_outcome_id,
            )
            .filter(
                POPEOMapping.peo_id == peo_id,
                Attainment.semester == semester,
                Attainment.academic_year == academic_year,
            )
            .all()
        )

        if not records:
            raise Exception("No PO Attainments found")

        weighted_sum = 0
        total_weight = 0

        for attainment, mapping_level in records:
            weighted_sum += attainment * mapping_level
            total_weight += mapping_level

        peo_attainment = round(weighted_sum / total_weight, 2)

        return {
            "peo_id": peo_id,
            "attainment_percentage": peo_attainment,
            "attainment_level": (
                "High"
                if peo_attainment >= 70
                else "Medium"
                if peo_attainment >= 50
                else "Low"
            ),
        }