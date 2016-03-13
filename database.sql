CREATE TABLE cars (
    cars_id SERIAL PRIMARY KEY,
    make VARCHAR,
    model VARCHAR,
    year INTEGER,
    color VARCHAR,
    updated TIMESTAMP,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO falcon_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO falcon_user;