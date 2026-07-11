from pydantic import BaseModel


class CourseObjectiveCreate(BaseModel):
    subject_id: int
    objective_code: str
    description: str


class CourseObjectiveResponse(CourseObjectiveCreate):
    id: int

    class Config:
        from_attributes = True