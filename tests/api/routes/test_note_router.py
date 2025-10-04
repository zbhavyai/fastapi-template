import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_note_listing() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/note")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    ids = [item["id"] for item in data]
    assert "3282249b-19ee-4c5e-9be2-b9f714610aa6" in ids
    assert "1d7539f9-e9b7-4a06-9e6c-d5d6cf74d87a" in ids
    assert "e969ffd7-b4ce-47e1-8f43-8811ae576392" in ids


@pytest.mark.asyncio
async def test_note_get_by_id() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/note/1d7539f9-e9b7-4a06-9e6c-d5d6cf74d87a")

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Note 2"
    assert data["content"] == "Content 2"


@pytest.mark.asyncio
async def test_note_creation() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/note",
            json={"title": "Test note title", "content": "Test note description"},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test note title"
    assert data["content"] == "Test note description"
    assert "id" in data and data["id"]


@pytest.mark.asyncio
async def test_note_creation_with_null_title() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/note",
            json={"title": None, "content": "Test note description"},
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_note_update_title() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch(
            "/api/v1/note/1d7539f9-e9b7-4a06-9e6c-d5d6cf74d87a",
            json={"title": "Test updated title"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test updated title"


@pytest.mark.asyncio
async def test_note_update_content() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch(
            "/api/v1/note/1d7539f9-e9b7-4a06-9e6c-d5d6cf74d87a",
            json={"content": "Test updated content"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test updated content"


@pytest.mark.asyncio
async def test_note_update_does_not_exist() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch(
            "/api/v1/note/8aba169f-f901-4d71-94e2-1251690aa0c9",
            json={"title": "Does not matter"},
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_note_deletion() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete(
            "/api/v1/note/1d7539f9-e9b7-4a06-9e6c-d5d6cf74d87a",
        )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_note_deletion_does_not_exist() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete(
            "/api/v1/note/8aba169f-f901-4d71-94e2-1251690aa0c9",
        )

    assert response.status_code == 404
