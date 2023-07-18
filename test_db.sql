CREATE TABLE test(
	id				serial			NOT NULL,
	name			varchar(255)	NOT NULL,
	value			jsonb,
	date_update		timestamptz		NOT NULL,

	PRIMARY KEY(id)
);
