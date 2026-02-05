#!/bin/bash
set -e

# Configuration - use docker-compose service name for database connection
DB_SERVICE="${DB_SERVICE:-db}"
DB_NAME="${POSTGRES_DB:-taskdb}"
DB_USER="${POSTGRES_USER:-postgres}"

echo "Creating test table..."
docker-compose exec -T "$DB_SERVICE" psql -U "$DB_USER" -d "$DB_NAME" -c "CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name VARCHAR(100), city VARCHAR(100), state VARCHAR(50), occupation VARCHAR(100));"

echo "Inserting fake data..."
docker-compose exec -T "$DB_SERVICE" psql -U "$DB_USER" -d "$DB_NAME" -c "
INSERT INTO test (name, city, state, occupation) VALUES 
  ('John', 'New York', 'NY', 'Software Engineer'),
  ('Joanna', 'Los Angeles', 'CA', 'Data Scientist'),
  ('Jennifer', 'Chicago', 'IL', 'Product Manager'),
  ('Michael', 'Houston', 'TX', 'DevOps Engineer'),
  ('Sarah', 'Phoenix', 'AZ', 'UX Designer'),
  ('David', 'Philadelphia', 'PA', 'Backend Developer'),
  ('Emma', 'San Antonio', 'TX', 'Frontend Developer'),
  ('Robert', 'San Diego', 'CA', 'QA Engineer'),
  ('Lisa', 'Dallas', 'TX', 'Project Manager'),
  ('James', 'San Jose', 'CA', 'System Architect');
"

echo "Verifying data..."
docker-compose exec -T "$DB_SERVICE" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT COUNT(*) FROM test;"

echo "Done!"