import psycopg2

hostname = "localhost"
database = "postgres_cdc_dev"
user = "postgres"
password = ""

conn = psycopg2.connect(host=hostname, database=database, user=user, password=password)

tables = ["asset", "scenario", "scene", "object", "statistics", "text"]

table_creation_commands = [
    """
        CREATE TABLE asset (
            id SERIAL PRIMARY KEY,
            name VARCHAR(256) NOT NULL,
            s3_key VARCHAR(256) NOT NULL,
            obj_type VARCHAR(50) NOT NULL
        )
    """,
    """
        CREATE TABLE scenario (
            id SERIAL PRIMARY KEY,
            name VARCHAR(256) NOT NULL,
            friendly_name VARCHAR(256) NOT NULL,
            description VARCHAR(256) NOT NULL,
            scene_ids BIGINT[] NOT NULL,
            is_published BOOLEAN NOT NULL,
            is_archived BOOLEAN NOT NULL,
            is_previewable BOOLEAN NOT NULL,
            publish_link VARCHAR(256),
            preview_link VARCHAR(256),
            expected_solve_time VARCHAR(20)
        )
    """,
    """
        CREATE TABLE scene (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            objects_id BIGINT[] NOT NULL,
            position DOUBLE PRECISION[] NOT NULL,
            scale DOUBLE PRECISION[] NOT NULL,
            rotation DOUBLE PRECISION[] NOT NULL,
            background_id BIGINT NOT NULL,
            FOREIGN KEY(background_id) REFERENCES asset(id)
        )
    """,
    """
        CREATE TABLE text (
            id SERIAL PRIMARY KEY,
            content text NOT NULL,
            next_text_id BIGINT,
            object_id BIGINT NOT NULL
            -- FOREIGN KEY (object_id) REFERENCES object (id)
        )
    """,
]

cur = conn.cursor()

# Drop tables if they exist first
drop_command = "DROP TABLE IF EXISTS {tablename} CASCADE"
for table in tables:
    cur.execute(drop_command.format(tablename=table))

# Create the table with the schema
for command in table_creation_commands:
    cur.execute(command)

cur.close()
conn.commit()
