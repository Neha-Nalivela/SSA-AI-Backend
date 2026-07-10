from sqlalchemy.orm import Session

from app.models.program import Program
from app.schemas.program import ProgramCreate, ProgramUpdate


class ProgramService:

    @staticmethod
    def create_program(db: Session, data: ProgramCreate):

        program = db.query(Program).filter(
            Program.program_code == data.program_code
        ).first()

        if program:
            raise Exception("Program code already exists")

        new_program = Program(
            program_code=data.program_code,
            program_name=data.program_name,
            duration=data.duration
        )

        db.add(new_program)
        db.commit()
        db.refresh(new_program)

        return new_program

    @staticmethod
    def get_programs(db: Session):
        return db.query(Program).all()

    @staticmethod
    def get_program(db: Session, program_id: int):

        program = db.query(Program).filter(
            Program.id == program_id
        ).first()

        if not program:
            raise Exception("Program not found")

        return program

    @staticmethod
    def update_program(
        db: Session,
        program_id: int,
        data: ProgramUpdate
    ):

        program = db.query(Program).filter(
            Program.id == program_id
        ).first()

        if not program:
            raise Exception("Program not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(program, key, value)

        db.commit()
        db.refresh(program)

        return program

    @staticmethod
    def delete_program(db: Session, program_id: int):

        program = db.query(Program).filter(
            Program.id == program_id
        ).first()

        if not program:
            raise Exception("Program not found")

        db.delete(program)
        db.commit()

        return {"message": "Program deleted successfully"}