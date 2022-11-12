CREATE TYPE filetype AS ENUM ('Image', 'Video', 'Text', 'Manga', 'Other');
CREATE TYPE filestate AS ENUM ('processing', 'collision', 'private', 'public')
CREATE TABLE files (
    id BIGSERIAL PRIMARY KEY,
    hash CHARACTER VARYING(32) PRIMARY KEY,
    filename CHARACTER VARYING NOT NULL UNIQUE,
    owner CHARACTER VARYING REFERENCES users (username) ON DELETE SET NULL ON UPDATE CASCADE,
    description CHARACTER VARYING DEFAULT '',
    upload_time timestamp with time zone NOT NULL,
    size CHARACTER VARYING NOT NULL,
    type filetype NOT NULL DEFAULT 'Other',
    group_id UUID,
    state filestate NOT NULL DEFAULT 'processing'
);
CREATE UNIQUE INDEX ON files (hash) WHERE state = 'public';





CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category CHARACTER VARYING NOT NULL UNIQUE
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    tag CHARACTER VARYING NOT NULL UNIQUE,
    category_id INTEGER DEFAULT 1 REFERENCES categories (id) ON DELETE SET DEFAULT ON UPDATE CASCADE
);

CREATE TABLE files_tags (
    id SERIAL PRIMARY KEY,
    file_hash CHARACTER VARYING(32) REFERENCES files (hash) ON DELETE CASCADE ON UPDATE CASCADE,
    tag_id INTEGER REFERENCES tags (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE images (
    hash CHARACTER VARYING(32) PRIMARY KEY REFERENCES files (hash) ON DELETE CASCADE ON UPDATE CASCADE,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    phash BIGINT NOT NULL,
    colorhash BIGINT NOT NULL
);

CREATE TABLE videos (
    hash CHARACTER VARYING(32) PRIMARY KEY REFERENCES files (hash) ON DELETE CASCADE ON UPDATE CASCADE,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    has_audio BOOLEAN NOT NULL
);

CREATE TABLE stories (
    hash CHARACTER VARYING(32) PRIMARY KEY REFERENCES files (hash) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE mangas (
    hash CHARACTER VARYING(32) PRIMARY KEY REFERENCES files (hash) ON DELETE CASCADE ON UPDATE CASCADE
);

-- HAMMING:->>>>>   bit_count(phash # oth_phash) <<<<<--!!!!!!! # - XOR
-- select bit_count(images.phash::bit(64) # (-3906285507453321988)::bit(64)) from images left join files on images.hash=files.hash;