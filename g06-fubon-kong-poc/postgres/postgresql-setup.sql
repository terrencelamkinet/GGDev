-- Fubon HK Kong PoC PostgreSQL bootstrap
-- Run as a PostgreSQL superuser on the external RHEL PostgreSQL 14+ VM.
-- Replace the password before execution. Do not commit the real password.

CREATE USER kong WITH PASSWORD '__REPLACE_WITH_STRONG_PASSWORD__';
CREATE DATABASE kong OWNER kong;
GRANT ALL PRIVILEGES ON DATABASE kong TO kong;

\c kong
GRANT ALL ON SCHEMA public TO kong;
ALTER SCHEMA public OWNER TO kong;
