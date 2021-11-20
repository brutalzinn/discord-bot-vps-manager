-- Table: public.usuario

-- DROP TABLE IF EXISTS public.usuario;

CREATE TABLE IF NOT EXISTS grupos
(
    "id" integer PRIMARY KEY NOT NULL,
    "name" text,
    "descricao" text,
    "cargo" text,
    "alias" integer DEFAULT 0 NOT NULL
);
ALTER TABLE IF EXISTS grupos
    OWNER to root;

CREATE TABLE IF NOT EXISTS usuario
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    email text,
    discord_id text,
    senha text,
    token text,
    last_login timestamp NULL DEFAULT null,
    whitelist integer DEFAULT 0,
    nivel integer NOT NULL DEFAULT 0,
    CONSTRAINT usuario_pkey PRIMARY KEY (id),
    CONSTRAINT usuario_nivel_fkey FOREIGN KEY (nivel)
        REFERENCES grupos (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
SET TIMEZONE TO 'America/Sao_Paulo';

ALTER TABLE IF EXISTS usuario
    OWNER to root;

-- insert users test
INSERT INTO grupos(
	"id", "name", "descricao", "cargo", "alias")
    VALUES (0, 'normal', 'Usuários normais ficam por aqui.', 'jogador normal', 0);

INSERT INTO grupos(
	"id", "name", "descricao", "cargo", "alias")
    VALUES (1, 'membro', 'Usuários membros ficam por aqui.', 'jogador membro', 0);

INSERT INTO grupos(
	"id", "name", "descricao", "cargo", "alias")
    VALUES (2, 'moderador', 'Usuários moderadores ficam por aqui.', 'moderador', 0);

INSERT INTO grupos(
	"id", "name", "descricao", "cargo", "alias")
    VALUES (3, 'administrador', 'Usuários administradores ficam por aqui.', 'administrador', 0);
    
INSERT INTO usuario(
	"id", "email", "discord_id", "senha", "token" ,"last_login", "whitelist", "nivel")
    VALUES (DEFAULT, 'teste@example.com', 'robertocpaes.dev#2825', '$2y$10$kEuT6V6Tpbx9TsQNL3WHtuErmSm4/cwOnqoX.t1nB99VahkUy8sa.','','now', 0, 0);

INSERT INTO usuario(
	"id", "email", "discord_id", "senha", "token" ,"last_login", "whitelist", "nivel")
    VALUES (DEFAULT, 'teste@example.com', 'dani95ye#6699', '$2y$10$kEuT6V6Tpbx9TsQNL3WHtuErmSm4/cwOnqoX.t1nB99VahkUy8sa.','','now', 0, 0);

INSERT INTO usuario(
	"id", "email", "discord_id", "senha", "token" ,"last_login", "whitelist", "nivel")
    VALUES (DEFAULT, 'teste@example.com', 'luisph#3300', '$2y$10$kEuT6V6Tpbx9TsQNL3WHtuErmSm4/cwOnqoX.t1nB99VahkUy8sa.','','now', 0, 0);

--first groups
