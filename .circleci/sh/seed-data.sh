#!/bin/bash
set -e

# Configuration
DATABASE_URL="${TEST_DATABASE_URL:-postgresql://postgres:postgres@localhost:5432/taskdb}"

echo "Creating test table..."
psql -d "$DATABASE_URL" -c "CREATE TABLE IF NOT EXISTS test (name char(25));"

echo "Inserting fake data..."
psql -d "$DATABASE_URL" -c "
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
psql -d "$DATABASE_URL" -c "SELECT COUNT(*) FROM test;"

echo "Done!"