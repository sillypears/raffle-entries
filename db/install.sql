
-- Database: postgres

-- DROP DATABASE IF EXISTS raffle_entries;

CREATE DATABASE raffle_entries
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE postgres
    IS 'default administrative connection database';
-
CREATE DATABASE raffle_entries
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

GRANT ALL ON DATABASE raffle_entries TO pg_database_owner;
-- Table: public.makers

-- DROP TABLE IF EXISTS public.makers;

CREATE TABLE public.makers
(
    id serial NOT NULL,
    name character(50) NOT NULL,
    display character(200) NOT NULL,
    CONSTRAINT maker_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.makers
    OWNER to postgres;

-- Table: public.entries

-- DROP TABLE IF EXISTS public.entries;
CREATE TABLE public.entries
(
    id serial NOT NULL,
    maker_id integer NOT NULL,
    epoch integer NOT NULL,
    raffle_link character(500) NOT NULL,
    notes text,
    result boolean NOT NULL DEFAULT false,
    CONSTRAINT entries_pkey PRIMARY KEY (id),
    CONSTRAINT maker_id_fkey FOREIGN KEY (maker_id)
        REFERENCES public.makers (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.entries
    OWNER to postgres;