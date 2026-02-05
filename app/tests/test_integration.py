import pytest
import asyncio
from app.database import Database

@pytest.mark.asyncio
async def test_database_connection():
    """Test database pool connection"""
    db = Database()
    await db.connect()
    assert db.pool is not None
    await db.disconnect()

@pytest.mark.asyncio
async def test_create_tables():
    """Test table creation"""
    db = Database()
    await db.connect()
    await db.create_tables()
    
    # Verify table exists
    async with db.pool.acquire() as conn:
        result = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'tasks'
            )
        """)
        assert result is True
    
    await db.disconnect()

@pytest.mark.asyncio
async def test_crud_operations():
    """Test full CRUD cycle"""
    db = Database()
    await db.connect()
    await db.create_tables()
    
    # Create
    task_id = await db.create_task("Test Task", "Description", False)
    assert task_id > 0
    
    # Read
    task = await db.get_task(task_id)
    assert task["title"] == "Test Task"
    assert task["completed"] is False
    
    # Update
    updated = await db.update_task(task_id, "Updated", "New desc", True)
    assert updated is True
    
    task = await db.get_task(task_id)
    assert task["title"] == "Updated"
    assert task["completed"] is True
    
    # Delete
    deleted = await db.delete_task(task_id)
    assert deleted is True
    
    task = await db.get_task(task_id)
    assert task is None
    
    await db.disconnect()