BEGIN;
CREATE TABLE "user"(
    "id" int PRIMARY KEY,
    "login" varchar UNIQUE NOT NULL,
    "display_name" varchar NOT NULL,
    "name" varchar,
    "surname" varchar,
    "patronymic" varchar,
    "creation_timestamp" timestamp NOT NULL DEFAULT (now()),
    "password_hash" varchar NOT NULL,
    "deleted" bool NOT NULL DEFAULT FALSE
);
CREATE TABLE "template"(
    "id" int PRIMARY KEY,
    "author_id" int NOT NULL,
    "workspace_id" int NOT NULL,
    "name" varchar NOT NULL,
    "description" text,
    "latex" text,
    "lua_example" text,
    "creation_timestamp" timestamp NOT NULL DEFAULT (now()),
    "edit_timestamp" timestamp NOT NULL DEFAULT (now()),
    "deleted" bool NOT NULL DEFAULT FALSE
);
CREATE TABLE "tickets_set"(
    "id" int PRIMARY KEY,
    "author_id" int NOT NULL,
    "template_id" int NOT NULL,
    "name" varchar NOT NULL,
    "description" text,
    "lua" text,
    "creation_timestamp" timestamp NOT NULL DEFAULT (now()),
    "edit_timestamp" timestamp NOT NULL DEFAULT (now()),
    "deleted" bool NOT NULL DEFAULT FALSE
);
CREATE TABLE "workspace"(
    "id" int PRIMARY KEY,
    "creator_id" int NOT NULL,
    "admin_id" int NOT NULL,
    "name" varchar NOT NULL,
    "description" text,
    "creation_timestamp" timestamp NOT NULL DEFAULT (now()),
    "deleted" bool NOT NULL DEFAULT FALSE
);
ALTER TABLE "template"
    ADD FOREIGN KEY ("author_id") REFERENCES "user"("id");
ALTER TABLE "template"
    ADD FOREIGN KEY ("workspace_id") REFERENCES "workspace"("id");
ALTER TABLE "tickets_set"
    ADD FOREIGN KEY ("author_id") REFERENCES "user"("id");
ALTER TABLE "tickets_set"
    ADD FOREIGN KEY ("template_id") REFERENCES "template"("id");
ALTER TABLE "workspace"
    ADD FOREIGN KEY ("creator_id") REFERENCES "user"("id");
ALTER TABLE "workspace"
    ADD FOREIGN KEY ("admin_id") REFERENCES "user"("id");
CREATE TABLE "user_workspace"(
    "user_id" int,
    "workspace_id" int,
    PRIMARY KEY ("user_id", "workspace_id")
);
ALTER TABLE "user_workspace"
    ADD FOREIGN KEY ("user_id") REFERENCES "user"("id");
ALTER TABLE "user_workspace"
    ADD FOREIGN KEY ("workspace_id") REFERENCES "workspace"("id");
COMMIT;

