from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate


def calculate_reliability(data: FeedbackCreate):

    score = 100

    ratings = [
        data.teaching_rating,
        data.clarity_rating,
        data.interaction_rating,
        data.practical_rating,
        data.assessment_rating
    ]

    # Submitted too quickly
    if data.completion_time < 30:
        score -= 30

    # All ratings identical
    if len(set(ratings)) == 1:
        score -= 20

    # Empty suggestion
    if not data.suggestions:
        score -= 10

    # Empty difficult topic
    if not data.difficult_topic:
        score -= 10

    return max(score, 0)


def create_feedback(db: Session, data: FeedbackCreate):

    reliability = calculate_reliability(data)

    feedback = Feedback(
        **data.model_dump(),
        reliability_score=reliability
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback