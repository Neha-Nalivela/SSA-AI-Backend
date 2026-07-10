from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


class AttendanceService:

    @staticmethod
    def create_attendance(db: Session, data: AttendanceCreate):

        percentage = (
            (data.attended_classes / data.total_classes) * 100
            if data.total_classes > 0 else 0
        )

        attendance = Attendance(
            student_id=data.student_id,
            subject_id=data.subject_id,
            total_classes=data.total_classes,
            attended_classes=data.attended_classes,
            attendance_percentage=round(percentage, 2),
            semester=data.semester,
            academic_year=data.academic_year
        )

        db.add(attendance)
        db.commit()
        db.refresh(attendance)

        return attendance

    @staticmethod
    def get_attendance(db: Session):
        return db.query(Attendance).all()

    @staticmethod
    def get_attendance_by_id(db: Session, attendance_id: int):

        attendance = db.query(Attendance).filter(
            Attendance.id == attendance_id
        ).first()

        if not attendance:
            raise Exception("Attendance not found")

        return attendance

    @staticmethod
    def update_attendance(
        db: Session,
        attendance_id: int,
        data: AttendanceUpdate
    ):

        attendance = db.query(Attendance).filter(
            Attendance.id == attendance_id
        ).first()

        if not attendance:
            raise Exception("Attendance not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(attendance, key, value)

        attendance.attendance_percentage = round(
            (attendance.attended_classes / attendance.total_classes) * 100,
            2
        ) if attendance.total_classes > 0 else 0

        db.commit()
        db.refresh(attendance)

        return attendance

    @staticmethod
    def delete_attendance(db: Session, attendance_id: int):

        attendance = db.query(Attendance).filter(
            Attendance.id == attendance_id
        ).first()

        if not attendance:
            raise Exception("Attendance not found")

        db.delete(attendance)
        db.commit()

        return {"message": "Attendance deleted successfully"}