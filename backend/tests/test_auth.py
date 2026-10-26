from fastapi.testclient import TestClient


def test_register_logs_in_and_never_returns_password(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register",
        json={
            "email": " New@Example.com ",
            "password": "password123",
            "nickname": " 새사용자 ",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["user"]["email"] == "new@example.com"
    assert body["user"]["nickname"] == "새사용자"
    assert "password" not in str(body).lower()

    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {body['token']}"})
    assert me.status_code == 200
    assert me.json()["email"] == "new@example.com"


def test_registration_rules_and_duplicates(client: TestClient) -> None:
    first = client.post(
        "/api/auth/register",
        json={"email": "one@example.com", "password": "password123", "nickname": "사용자1"},
    )
    assert first.status_code == 201

    duplicate_email = client.post(
        "/api/auth/register",
        json={"email": "ONE@example.com", "password": "password123", "nickname": "사용자2"},
    )
    assert duplicate_email.status_code == 409

    duplicate_nickname = client.post(
        "/api/auth/register",
        json={"email": "two@example.com", "password": "password123", "nickname": "사용자1"},
    )
    assert duplicate_nickname.status_code == 409

    invalid = client.post(
        "/api/auth/register",
        json={"email": "not-email", "password": "short", "nickname": "잘못된 닉네임"},
    )
    assert invalid.status_code == 422
    assert all("input" not in detail for detail in invalid.json()["error"]["details"])


def test_login_and_nickname_change(client: TestClient) -> None:
    client.post(
        "/api/auth/register",
        json={"email": "login@example.com", "password": "password123", "nickname": "로그인사용자"},
    )

    failure = client.post(
        "/api/auth/login", json={"email": "login@example.com", "password": "wrong-password"}
    )
    assert failure.status_code == 401
    assert "이메일 또는 비밀번호" in failure.json()["error"]["message"]

    login = client.post(
        "/api/auth/login", json={"email": "login@example.com", "password": "password123"}
    )
    headers = {"Authorization": f"Bearer {login.json()['token']}"}
    changed = client.patch(
        "/api/auth/me/nickname", json={"nickname": "바뀐_닉네임"}, headers=headers
    )
    assert changed.status_code == 200
    assert changed.json()["nickname"] == "바뀐_닉네임"


def test_protected_api_requires_login(client: TestClient) -> None:
    assert client.get("/api/studies").status_code == 401
    assert client.get("/api/todos").status_code == 401
    assert client.get("/api/errors").status_code == 401
