-- CREATE DATABASE test_betting_screenshots_bot
-- 	WITH
--     OWNER = postgres
--     ENCODING = 'UTF8'
-- 	LC_COLLATE = 'Russian_Russia.1251'
--     LC_CTYPE = 'Russian_Russia.1251'
-- 	TEMPLATE=template0
-- 	TABLESPACE = pg_default
--     CONNECTION LIMIT = -1
--     IS_TEMPLATE = False;
--

CREATE TABLE IF NOT EXISTS matches
(
    id INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    bookmaker_name VARCHAR(255) NOT NULL,
    start_at INT NOT NULL,
    bookmaker TEXT NOT NULL,
    bets TEXT,
    general TEXT,
    result TEXT,
	PRIMARY KEY(id)
);