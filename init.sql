-- Table: public.usuario

-- DROP TABLE IF EXISTS public.usuario;

CREATE TABLE IF NOT EXISTS public.usuario
(
    "id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "email" text,
    "discord_id" text,
    "senha" text,
    "nivel" integer DEFAULT 0 NOT NULL,
    CONSTRAINT usuario_pkey PRIMARY KEY ("id")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.usuario
    OWNER to root;

INSERT INTO public.usuario(
	"id", "email", "discord_id", "senha", "nivel")
    VALUES (DEFAULT, 'teste@example.com', 'robertocpaes.dev#2825', '$2y$10$kEuT6V6Tpbx9TsQNL3WHtuErmSm4/cwOnqoX.t1nB99VahkUy8sa.', 0);