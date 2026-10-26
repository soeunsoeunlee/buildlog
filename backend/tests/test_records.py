from fastapi.testclient import TestClient


def register(client: TestClient, email: str, nickname: str) -> dict[str, str]:
    response = client.post(
        "/api/auth/register",
        json={"email": email, "password": "password123", "nickname": nickname},
    )
    return {"Authorization": f"Bearer {response.json()['token']}"}


def test_study_crud_search_and_permissions(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    created = client.post(
        "/api/studies",
        json={"title": "  FastAPI 학습  ", "content": "  라우터와 테스트 정리  "},
        headers=auth_headers,
    )
    assert created.status_code == 201
    record = created.json()
    assert record["title"] == "FastAPI 학습"
    assert record["content"] == "라우터와 테스트 정리"
    assert record["is_public"] is False

    found = client.get("/api/studies?q=테스트", headers=auth_headers)
    assert [item["id"] for item in found.json()] == [record["id"]]

    updated = client.put(
        f"/api/studies/{record['id']}",
        json={"title": "수정 제목", "content": "수정 내용", "is_public": True},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["is_public"] is True

    other_headers = register(client, "other@example.com", "다른사용자")
    forbidden = client.put(
        f"/api/studies/{record['id']}",
        json={"title": "침범", "content": "수정 불가", "is_public": True},
        headers=other_headers,
    )
    assert forbidden.status_code == 403

    deleted = client.delete(f"/api/studies/{record['id']}", headers=auth_headers)
    assert deleted.status_code == 204
    assert client.get(f"/api/studies/{record['id']}", headers=auth_headers).status_code == 404


def test_private_study_is_hidden_from_another_user(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    record_id = client.post(
        "/api/studies",
        json={"title": "비공개", "content": "나만 보는 기록"},
        headers=auth_headers,
    ).json()["id"]
    other_headers = register(client, "viewer@example.com", "조회사용자")

    assert client.get(f"/api/studies/{record_id}", headers=other_headers).status_code == 404


def test_todo_filters_order_and_completion_time(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    first = client.post("/api/todos", json={"title": "첫 할 일"}, headers=auth_headers).json()
    second = client.post("/api/todos", json={"title": "둘째 할 일"}, headers=auth_headers).json()

    completed = client.patch(
        f"/api/todos/{second['id']}/status",
        json={"is_completed": True},
        headers=auth_headers,
    )
    assert completed.json()["is_completed"] is True
    assert completed.json()["completed_at"] is not None

    all_items = client.get("/api/todos", headers=auth_headers).json()
    assert [item["id"] for item in all_items] == [first["id"], second["id"]]
    assert len(client.get("/api/todos?state=pending", headers=auth_headers).json()) == 1
    assert len(client.get("/api/todos?state=completed", headers=auth_headers).json()) == 1

    reopened = client.patch(
        f"/api/todos/{second['id']}/status",
        json={"is_completed": False},
        headers=auth_headers,
    )
    assert reopened.json()["completed_at"] is None


def test_error_search_resolution_rules_and_reopen(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    created = client.post(
        "/api/errors",
        json={"title": "모듈 오류", "content": "모듈을 찾지 못함", "solution": ""},
        headers=auth_headers,
    )
    assert created.status_code == 201
    record = created.json()
    assert record["is_resolved"] is False
    assert record["solution"] is None

    invalid = client.put(
        f"/api/errors/{record['id']}",
        json={
            "title": record["title"],
            "content": record["content"],
            "solution": "",
            "is_resolved": True,
            "is_public": False,
        },
        headers=auth_headers,
    )
    assert invalid.status_code == 422

    resolved = client.put(
        f"/api/errors/{record['id']}",
        json={
            "title": record["title"],
            "content": record["content"],
            "solution": "backend 폴더에서 실행",
            "is_resolved": True,
            "is_public": False,
        },
        headers=auth_headers,
    )
    assert resolved.status_code == 200
    assert resolved.json()["resolved_at"] is not None
    assert len(client.get("/api/errors?state=resolved&q=모듈", headers=auth_headers).json()) == 1

    reopened = client.put(
        f"/api/errors/{record['id']}",
        json={
            "title": record["title"],
            "content": record["content"],
            "solution": "backend 폴더에서 실행",
            "is_resolved": False,
            "is_public": False,
        },
        headers=auth_headers,
    )
    assert reopened.json()["solution"] == "backend 폴더에서 실행"
    assert reopened.json()["resolved_at"] is None
