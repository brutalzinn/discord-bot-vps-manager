-- Table: public.usuario

-- DROP TABLE IF EXISTS public.usuario;

CREATE TABLE IF NOT EXISTS public.usuario
(
    "Id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Email" text,
    "Discord_Id" text,
    "Senha" text,
    "Nivel" integer DEFAULT 0 NOT NULL,
    CONSTRAINT usuario_pkey PRIMARY KEY ("Id")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.usuario
    OWNER to root;

INSERT INTO public.usuario(
	"Id", "Email", "Discord_Id", "Senha", "Nivel")
    VALUES (DEFAULT, 'teste@example.com', 'robertocpaes.dev#2825', '$2y$10$kEuT6V6Tpbx9TsQNL3WHtuErmSm4/cwOnqoX.t1nB99VahkUy8sa.', 0);