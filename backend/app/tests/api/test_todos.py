from fastapi.testclient import TestClient
from app.tests.utils.utils import get_token_headers
from app.core.config import settings
from app.tests.conftest import db
from app.tests.utils.user import create_random_user


# def test_create_todo(client: TestClient):
#     test_user = create_random_user()
#     test_todo = {
#         "title": "Test Todo",
#         "content": "Test Content",
#         "status": "todo",
#         "priority": "low",
#     }

#     headers = get_token_headers(test_user["email"])

#     response = client.post(
#         f"{settings.API_V1_STR}/todos/create", json=test_todo, headers=headers
#     )

#     assert response.status_code == 200
#     assert response.json()["success"] is True
#     assert response.json()["data"]["title"] == test_todo["title"]
#     assert response.json()["data"]["user_id"] == test_user["id"]
#     assert response.json()["message"] == "Todo created successfully"


def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Server is running!!!"
