from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"


def create_access_token(data: dict):

    payload = data.copy()

    payload["exp"] = datetime.utcnow() + timedelta(hours=24)

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )