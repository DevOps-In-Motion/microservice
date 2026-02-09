Build Status: [![CircleCI](https://dl.circleci.com/status-badge/img/gh/DevOps-In-Motion/microservice/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/DevOps-In-Motion/microservice/tree/main)


# FastAPI Task Management API

A simple REST API built with FastAPI and PostgreSQL for managing tasks.


## Features

- Create, read, update, and delete tasks
- PostgreSQL database integration
- Async operations with asyncpg
- Comprehensive test suite
- Docker containerization

## API Endpoints

- `GET /` - Health check
- `GET /tasks` - List all tasks
- `GET /tasks/{id}` - Get a specific task
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task

## Local Development

### Using Docker Compose

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=taskdb postgres:15-alpine

# Run tests
pytest
```

## Task Schema

```json
{
  "id": 1,
  "title": "Example Task",
  "description": "Task description",
  "completed": false
}
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string (default: `postgresql://postgres:postgres@localhost:5432/taskdb`)

