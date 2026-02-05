import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import app

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def client():
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_db():
    """Mock database for testing"""
    with patch('main.db') as mock:
        yield mock


async def test_get_all_tasks(client, mock_db):
    """Test retrieving all tasks"""
    # Mock database response
    mock_db.get_all_tasks = AsyncMock(return_value=[
        {"id": 1, "title": "Task 1", "description": "Desc 1", "completed": False},
        {"id": 2, "title": "Task 2", "description": "Desc 2", "completed": True}
    ])
    
    response = await client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["completed"] is True


async def test_get_task_by_id(client, mock_db):
    """Test retrieving a specific task"""
    # Mock database response
    mock_db.get_task = AsyncMock(return_value={
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    })
    
    response = await client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Task"
    assert data["completed"] is False


async def test_get_task_not_found(client, mock_db):
    """Test retrieving a task that doesn't exist"""
    # Mock database returning None
    mock_db.get_task = AsyncMock(return_value=None)
    
    response = await client.get("/tasks/999")
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]


async def test_create_task(client, mock_db):
    """Test creating a new task"""
    # Mock database response
    mock_db.create_task = AsyncMock(return_value=123)
    
    task_data = {
        "title": "New Task",
        "description": "New Description",
        "completed": False
    }
    
    response = await client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 123
    assert data["title"] == "New Task"
    assert data["description"] == "New Description"
    assert data["completed"] is False
    
    # Verify database method was called with correct parameters
    mock_db.create_task.assert_called_once_with("New Task", "New Description", False)


async def test_update_task(client, mock_db):
    """Test updating a task"""
    # Mock database response
    mock_db.update_task = AsyncMock(return_value=True)
    mock_db.get_task = AsyncMock(return_value={
        "id": 1,
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True
    })
    
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True
    }
    
    response = await client.put("/tasks/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Updated Task"
    assert data["completed"] is True
    
    # Verify database method was called with correct parameters
    mock_db.update_task.assert_called_once_with(1, "Updated Task", "Updated Description", True)


async def test_update_task_not_found(client, mock_db):
    """Test updating a task that doesn't exist"""
    # Mock database returning False (task not found)
    mock_db.update_task = AsyncMock(return_value=False)
    
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True
    }
    
    response = await client.put("/tasks/999", json=update_data)
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]


async def test_delete_task(client, mock_db):
    """Test deleting a task"""
    # Mock database response
    mock_db.delete_task = AsyncMock(return_value=True)
    
    response = await client.delete("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task deleted successfully"
    
    # Verify database method was called with correct parameters
    mock_db.delete_task.assert_called_once_with(1)


async def test_delete_task_not_found(client, mock_db):
    """Test deleting a task that doesn't exist"""
    # Mock database returning False (task not found)
    mock_db.delete_task = AsyncMock(return_value=False)
    
    response = await client.delete("/tasks/999")
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]


async def test_create_task_with_minimal_data(client, mock_db):
    """Test creating a task with only required fields"""
    # Mock database response
    mock_db.create_task = AsyncMock(return_value=456)
    
    task_data = {
        "title": "Minimal Task"
    }
    
    response = await client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 456
    assert data["title"] == "Minimal Task"
    assert data["description"] is None  # Default value
    assert data["completed"] is False  # Default value


async def test_get_empty_tasks_list(client, mock_db):
    """Test retrieving tasks when none exist"""
    # Mock database returning empty list
    mock_db.get_all_tasks = AsyncMock(return_value=[])
    
    response = await client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

