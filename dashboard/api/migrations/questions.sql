CREATE TABLE
	IF NOT EXISTS questions (
		id UUID PRIMARY KEY DEFAULT uuidv4 (),
		text TEXT NOT NULL,
		type TEXT NOT NULL CHECK (type IN ('freeform', 'multichoice')),
		ans TEXT,
		choices TEXT ARRAY,
		CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES tutors (id),
		created_at TIMESTAMPTZ NOT NULL DEFAULT NOW (),
		deleted_at TIMESTAMPTZ,
		updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW ()
	);
