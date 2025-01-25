-- Create the postgres user if it doesn't already exist
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'postgres') THEN
      CREATE USER postgres WITH PASSWORD 'password';
      GRANT ALL PRIVILEGES ON DATABASE scanner_db TO postgres;
      ALTER USER postgres WITH SUPERUSER;
   END IF;
END
$do$;

-- Create the scanner_db database if it doesn't already exist
CREATE DATABASE scanner_db
   WITH OWNER = postgres
   ENCODING = 'UTF8'
   CONNECTION LIMIT = -1;

-- Ensure the tokens table exists
\connect scanner_db postgres
CREATE TABLE IF NOT EXISTS token (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    symbol VARCHAR NOT NULL,
    market_cap FLOAT,
    transactions INT
);