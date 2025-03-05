from datetime import timedelta
import random
import string

from app.core.security import create_access_token


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_token_headers(email: str) -> dict[str, str]:
    token = create_access_token(subject=email, expires_delta=timedelta(minutes=15))

    headers = {
        "Cookie": f"access_token={token}",
    }
    return headers
