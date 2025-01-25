CREATE TABLE IF NOT EXISTS token (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    symbol VARCHAR NOT NULL,
    market_cap FLOAT,
    transactions INT
);