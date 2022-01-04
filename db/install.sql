
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

GRANT ALL ON DATABASE raffle_entries TO pg_database_owner;
-- Table: public.makers

-- DROP TABLE IF EXISTS public.makers;


CREATE TABLE IF NOT EXISTS public.makers
(
    id serial NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    display character varying(200) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT makers_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;


-- Table: public.entries

-- DROP TABLE IF EXISTS public.entries;
CREATE TABLE IF NOT EXISTS public.entries
(
    id serial NOT NULL,
    maker_id integer NOT NULL,
    epoch integer NOT NULL,
    raffle_link character varying(500) COLLATE pg_catalog."default" NOT NULL,
    notes text COLLATE pg_catalog."default",
    result boolean NOT NULL DEFAULT false,
    date date NOT NULL,
    CONSTRAINT entries_pkey PRIMARY KEY (id),
    CONSTRAINT maker_id_fkey FOREIGN KEY (maker_id)
        REFERENCES public.makers (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.entries
    OWNER to postgres;

-- View: public.all_entries

-- DROP VIEW public.all_entries;

CREATE OR REPLACE VIEW public.all_entries
 AS
 SELECT m.display AS maker,
    e.result,
    e.epoch,
    e.date,
    e.notes,
    e.raffle_link AS info,
    e.id,
    m.id AS "maker id"
   FROM entries e
     LEFT JOIN makers m ON e.maker_id = m.id;

ALTER TABLE public.all_entries
    OWNER TO postgres;

