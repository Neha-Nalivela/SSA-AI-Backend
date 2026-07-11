from pydantic import BaseModel


class ProgramObjectiveBase(BaseModel):
    program_id: int
    objective_code: str
    description: str


class ProgramObjectiveCreate(ProgramObjectiveBase):
    pass


class ProgramObjectiveUpdate(ProgramObjectiveBase):
    pass


class ProgramObjectiveResponse(ProgramObjectiveBase):
    id: int

    class Config:
        from_attributes = True