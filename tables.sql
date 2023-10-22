CREATE TABLE IF NOT EXISTS public.employers
(
    id integer NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    hh_url character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT employers_pkey PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.vacancies
(
    id integer NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    hh_url character varying(255) COLLATE pg_catalog."default" NOT NULL,
    area character varying(255) COLLATE pg_catalog."default" NOT NULL,
    employer_id integer NOT NULL,
    experience character varying(255) COLLATE pg_catalog."default" NOT NULL,
    salary_currency character varying(255) COLLATE pg_catalog."default",
    salary_from integer,
    salary_to integer,
    requirement text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT vacancies_pkey PRIMARY KEY (id),
    CONSTRAINT fk_vacancies_employers FOREIGN KEY (employer_id)
        REFERENCES public.employers (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)