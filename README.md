# FastAPI Task Management API

A simple REST API built with FastAPI and PostgreSQL for managing tasks.

[https://circleci.com/gh/DevOps-In-Motion/microservice](https://circleci.com/gh/DevOps-In-Motion/microservice){: target="_blank"}

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

    - exists in a public VCS repo connected to CircleCI
    uses a custom docker image generated during the pipeline
    performs testing with results that can be collected by CircleCI
    includes use of a database such as postgres, mysql, or mongodb
    make use of a “sidecar” or secondary container for this
    DB container may be off-the-shelf image
    performs conditional work during the execution of the pipeline to limit unnecessary work (may be based on PR status, files changes, success or failures of upstream work)
    includes shell scripting and non-scripting language (either as the application under test, or in config file)
    publishes an artifact to PaaS, FaaS, or IaaS of your choice
    only on merge to default branch
    credentials may no be accessible outside of approved builds
    ideally makes use of OIDC

Once you are satisfied, and have a working (green) build, please submit a brief writeup and submit it to the link below. The writeup should be written as if directed towards a customer looking for a reference pipeline.

    Include link to the VCS Repo, and a passing CCI build link.
    Explain the overall architecture
    what it does
    how components are mapped together
    Explain the unique value and optimizations made leveraging CircleCI features
    Outline potential future optimizations or trade-offs to consider
