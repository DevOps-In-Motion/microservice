import os
import asyncpg
from typing import List, Optional, Dict


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.db_url = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/taskdb"
        )

    async def connect(self):
        """Create connection pool"""
        self.pool = await asyncpg.create_pool(self.db_url, min_size=1, max_size=10)

    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()

    async def create_tables(self):
        """Create tasks table if it doesn't exist"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    async def get_all_tasks(self) -> List[Dict]:
        """Retrieve all tasks"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT id, title, description, completed FROM tasks ORDER BY id")
            return [dict(row) for row in rows]

    async def get_task(self, task_id: int) -> Optional[Dict]:
        """Retrieve a single task by ID"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, title, description, completed FROM tasks WHERE id = $1",
                task_id
            )
            return dict(row) if row else None

    async def create_task(self, title: str, description: Optional[str], completed: bool) -> int:
        """Create a new task"""
        async with self.pool.acquire() as conn:
            task_id = await conn.fetchval(
                """
                INSERT INTO tasks (title, description, completed)
                VALUES ($1, $2, $3)
                RETURNING id
                """,
                title, description, completed
            )
            return task_id

    async def update_task(self, task_id: int, title: str, description: Optional[str], completed: bool) -> bool:
        """Update an existing task"""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE tasks
                SET title = $1, description = $2, completed = $3
                WHERE id = $4
                """,
                title, description, completed, task_id
            )
            return result.split()[-1] == "1"

    async def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        async with self.pool.acquire() as conn:
            result = await conn.execute("DELETE FROM tasks WHERE id = $1", task_id)
            return result.split()[-1] == "1"
