#!/bin/bash
set -e

# Configuration - use docker-compose service name for database connection
DB_SERVICE="${DB_SERVICE:-db}"
DB_NAME="${POSTGRES_DB:-taskdb}"
DB_USER="${POSTGRES_USER:-postgres}"

echo "Creating test table..."
docker-compose exec -T "$DB_SERVICE" psql -U "$DB_USER" -d "$DB_NAME" -c "CREATE TABLE IF NOT EXISTS test (name char(25));"

echo "Inserting fake data..."
docker-compose exec -T "$DB_SERVICE" psql -U "$DB_USER" -d "$DB_NAME" -c "
INSERT INTO test (name) VALUES 
  ('John'), 
  ('Joanna'), 
  ('Jennifer'),
  ('Michael'),
  ('Sarah'),
  ('David'),
  ('Emma'),
  ('Robert'),
  ('Lisa'),
  ('James');
"

echo "Verifying data..."
docker-compose exec -T "$DB_SERVICE" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT COUNT(*) FROM test;"

echo "Done!"