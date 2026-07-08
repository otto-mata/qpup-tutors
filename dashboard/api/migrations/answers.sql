CREATE TABLE
	IF NOT EXISTS answers (
		id UUID PRIMARY KEY DEFAULT uuidv4 (),
		value TEXT NOT NULL,
		correct BOOLEAN,
		CONSTRAINT fk_session FOREIGN KEY (session_id) REFERENCES sessions (id),
		CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id),
		created_at TIMESTAMPTZ NOT NULL DEFAULT NOW (),
		deleted_at TIMESTAMPTZ,
		updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW ()
	);
