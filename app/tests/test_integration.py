import pytest
import pytest_asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from db import Database

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def db():
    """Database fixture that handles connection and cleanup"""
    database = Database()
    await database.connect()
    await database.create_tables()
    yield database
    # Cleanup: drop all test data
    if database.pool is not None:
        async with database.pool.acquire() as conn:
            await conn.execute("DELETE FROM tasks")
        await database.disconnect()


async def test_database_connection(db):
    """Test database pool connection"""
    assert db.pool is not None
    assert db.pool.get_size() > 0


async def test_create_tables(db):
    """Test table creation"""
    # Verify table exists
    async with db.pool.acquire() as conn:
        result = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'tasks'
            )
        """)
        assert result is True


async def test_create_task(db):
    """Test creating a new task"""
    task_id = await db.create_task("Test Task", "Test Description", False)
    assert task_id > 0
    
    # Verify task was created
    task = await db.get_task(task_id)
    assert task is not None
    assert task["title"] == "Test Task"
    assert task["description"] == "Test Description"
    assert task["completed"] is False


async def test_get_task(db):
    """Test retrieving a task"""
    # Create a task first
    task_id = await db.create_task("Find Me", "Description", False)
    
    # Retrieve it
    task = await db.get_task(task_id)
    assert task is not None
    assert task["id"] == task_id
    assert task["title"] == "Find Me"
    assert task["completed"] is False


async def test_get_task_not_found(db):
    """Test retrieving a task that doesn't exist"""
    task = await db.get_task(99999)
    assert task is None


async def test_get_all_tasks(db):
    """Test retrieving all tasks"""
    # Create multiple tasks
    await db.create_task("Task 1", "Desc 1", False)
    await db.create_task("Task 2", "Desc 2", True)
    await db.create_task("Task 3", None, False)
    
    # Retrieve all
    tasks = await db.get_all_tasks()
    assert len(tasks) >= 3
    
    # Verify structure
    for task in tasks:
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task


async def test_update_task(db):
    """Test updating a task"""
    # Create a task
    task_id = await db.create_task("Original", "Original Desc", False)
    
    # Update it
    updated = await db.update_task(task_id, "Updated", "New Desc", True)
    assert updated is True
    
    # Verify update
    task = await db.get_task(task_id)
    assert task["title"] == "Updated"
    assert task["description"] == "New Desc"
    assert task["completed"] is True


async def test_update_task_not_found(db):
    """Test updating a task that doesn't exist"""
    updated = await db.update_task(99999, "Title", "Desc", False)
    assert updated is False


async def test_delete_task(db):
    """Test deleting a task"""
    # Create a task
    task_id = await db.create_task("Delete Me", "Description", False)
    
    # Verify it exists
    task = await db.get_task(task_id)
    assert task is not None
    
    # Delete it
    deleted = await db.delete_task(task_id)
    assert deleted is True
    
    # Verify it's gone
    task = await db.get_task(task_id)
    assert task is None


async def test_delete_task_not_found(db):
    """Test deleting a task that doesn't exist"""
    deleted = await db.delete_task(99999)
    assert deleted is False


async def test_crud_operations(db):
    """Test full CRUD cycle"""
    # Create
    task_id = await db.create_task("CRUD Test", "Full cycle test", False)
    assert task_id > 0
    
    # Read
    task = await db.get_task(task_id)
    assert task["title"] == "CRUD Test"
    assert task["completed"] is False
    
    # Update
    updated = await db.update_task(task_id, "Updated CRUD", "Modified", True)
    assert updated is True
    
    task = await db.get_task(task_id)
    assert task["title"] == "Updated CRUD"
    assert task["completed"] is True
    
    # Delete
    deleted = await db.delete_task(task_id)
    assert deleted is True
    
    task = await db.get_task(task_id)
    assert task is None

