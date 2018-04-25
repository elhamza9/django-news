CREATE ROLE djangonews WITH LOGIN PASSWORD 'djangonewspass';
CREATE DATABASE djangonews_db;
GRANT ALL PRIVILEGES ON DATABASE djangonews_db TO djangonews;
