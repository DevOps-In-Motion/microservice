import pytest
from httpx import AsyncClient
from main import app
import os

# Set test database URL
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/taskdb"


@pytest.fixture
async def client():
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root(client):
    """Test health check endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_task(client):
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }
    response = await client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_get_tasks(client):
    """Test retrieving all tasks"""
    response = await client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_task_by_id(client):
    """Test retrieving a specific task"""
    # First create a task
    task_data = {"title": "Find Me", "description": "Test", "completed": False}
    create_response = await client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Now retrieve it
    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"


@pytest.mark.asyncio
async def test_update_task(client):
    """Test updating a task"""
    # Create a task first
    task_data = {"title": "Original", "description": "Test", "completed": False}
    create_response = await client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Update it
    update_data = {"title": "Updated", "description": "Modified", "completed": True}
    response = await client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["completed"] is True


@pytest.mark.asyncio
async def test_delete_task(client):
    """Test deleting a task"""
    # Create a task first
    task_data = {"title": "Delete Me", "description": "Test", "completed": False}
    create_response = await client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Delete it
    response = await client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = await client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_task(client):
    """Test retrieving a task that doesn't exist"""
    response = await client.get("/tasks/99999")
    assert response.status_code == 404
