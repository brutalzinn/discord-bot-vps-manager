-- Table: public.usuario

-- DROP TABLE IF EXISTS public.usuario;

CREATE TABLE IF NOT EXISTS public.usuario
(
    "Id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Email" text COLLATE pg_catalog."default",
    "Discord_Id" text COLLATE pg_catalog."default",
    "Senha" text COLLATE pg_catalog."default",
    CONSTRAINT usuario_pkey PRIMARY KEY ("Id")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.usuario
    OWNER to root;