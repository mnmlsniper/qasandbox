import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from config import AUTH_USERNAME, AUTH_PASSWORD, JWT_SECRET, JWT_ALGORITHM, JWT_TTL_HOURS

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Проверяет наличие токена в заголовке Authorization.
    Фактическая валидация токена происходит на фронтенде.
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


def check_credentials(username: str, password: str) -> bool:
    """Сверяет логин и пароль с учёткой из настроек (сравнение за постоянное время)."""
    return (
        secrets.compare_digest(username.encode(), AUTH_USERNAME.encode())
        and secrets.compare_digest(password.encode(), AUTH_PASSWORD.encode())
    )


def create_token(username: str) -> tuple[str, int]:
    """Выпускает JWT. Возвращает токен и срок его жизни в секундах."""
    ttl = timedelta(hours=JWT_TTL_HOURS)
    now = datetime.now(timezone.utc)
    payload = {"sub": username, "iat": now, "exp": now + ttl}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM), int(ttl.total_seconds())
