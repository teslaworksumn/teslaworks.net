-- Create Postgres tables for github.com/teslaworksumn/teslaworks.net

CREATE TABLE projects (
    project_id serial,
    name text,
    slug text,
    description text,
    photo_url text,
    past_project boolean NOT NULL DEFAULT FALSE,
    display_order integer,
    PRIMARY KEY (project_id)
);

CREATE TABLE leaders (
    leader_id serial,
    name text,
    email text,
    phone text,
    bio text,
    photo_url text,
    PRIMARY KEY (leader_id)
);

CREATE TABLE project_leaders (
    project_id integer
        NOT NULL
        REFERENCES projects
        ON DELETE CASCADE,
    leader_id integer
        NOT NULL
        REFERENCES leaders
        ON DELETE CASCADE,
    display_order integer,
    PRIMARY KEY (project_id, leader_id)
);

CREATE TABLE project_needs (
    project_need_id serial,
    project_id integer
        NOT NULL
        REFERENCES projects
        ON DELETE CASCADE,
    need_text text,
    display_order integer,
    PRIMARY KEY (project_need_id)
);

CREATE TABLE project_photos (
    project_photo_id serial,
    project_id integer
        NOT NULL
        REFERENCES projects
        ON DELETE CASCADE,
    photo_url text,
    display_order integer,
    PRIMARY KEY (project_photo_id)
);
