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




 
Create a CircleCI configuration that builds a tested docker image and publishes an artifact. The pipeline must meet the following criteria:

    - uses a custom docker image generated during the pipeline
    - only on merge to default branch

Once you are satisfied, and have a working (green) build, please submit a brief writeup and submit it to the link below. The writeup should be written as if directed towards a customer looking for a reference pipeline.

    - Include link to the VCS Repo, and a passing CCI build link.
    Explain the overall architecture
    what it does
    how components are mapped together
    Explain the unique value and optimizations made leveraging CircleCI features
    Outline potential future optimizations or trade-offs to consider
