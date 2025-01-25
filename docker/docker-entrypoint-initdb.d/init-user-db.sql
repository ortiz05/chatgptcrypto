-- Create the 'scanner_db' database if it doesn't already exist
CREATE DATABASE scanner_db;

-- Create the 'postgres' user with a password and grant permissions
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE scanner_db TO postgres;

-- Ensure the user has the necessary roles
ALTER USER postgres WITH SUPERUSER;
