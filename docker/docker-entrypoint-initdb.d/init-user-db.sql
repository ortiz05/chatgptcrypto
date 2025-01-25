CREATE USER postgres WITH PASSWORD 'password';
CREATE DATABASE scanner_db;
GRANT ALL PRIVILEGES ON DATABASE scanner_db TO postgres;
ALTER USER postgres WITH SUPERUSER;

CREATE TABLE IF NOT EXISTS token (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    symbol VARCHAR NOT NULL,
    market_cap FLOAT,
    transactions INT
);