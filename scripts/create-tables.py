import psycopg2

from app.config import config

hostname = config.get("postgres.hostname")
database = config.get("postgres.database")
user = config.get("postgres.user")
password = config.get("postgres.password", "")

conn = psycopg2.connect(host=hostname, database=database, user=user, password=password)

tables = config.get("script.table-order")

table_creation_commands = [
    """
        CREATE TABLE asset (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            s3_key TEXT NOT NULL,
            obj_type TEXT NOT NULL
        )
    """,
    """
        CREATE TABLE scenario (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            friendly_name TEXT NOT NULL,
            description TEXT NOT NULL,
            scene_ids BIGINT[] NOT NULL,
            is_published BOOLEAN NOT NULL,
            is_previewable BOOLEAN NOT NULL,
            publish_link TEXT,
            preview_link TEXT,
            expected_solve_time TEXT NOT NULL,
            introduction_data JSONB NOT NULL,
            conclusion_data JSONB NOT NULL,
            transitions JSONB[] NOT NULL
        )
    """,
    """
        CREATE TABLE scene (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            object_ids BIGINT[] NOT NULL,
            position DOUBLE PRECISION[] NOT NULL,
            scale DOUBLE PRECISION[] NOT NULL,
            rotation DOUBLE PRECISION[] NOT NULL,
            background_id BIGINT NOT NULL,
            camera_properties JSONB NOT NULL,
            hints TEXT[] NOT NULL,
            FOREIGN KEY(background_id) REFERENCES asset (id)
        )
    """,
    """
        CREATE TABLE object (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            position DOUBLE PRECISION[] NOT NULL,
            scale DOUBLE PRECISION[] NOT NULL,
            rotation DOUBLE PRECISION[] NOT NULL,
            asset_id BIGINT NOT NULL,
            next_objects JSONB[],
            texts TEXT[] NOT NULL,
            is_interactable BOOLEAN NOT NULL,
            animations_json JSONB NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES asset (id) ON DELETE CASCADE
        )
    """,
    """
        CREATE TABLE statistics (
            id SERIAL PRIMARY KEY,
            scenario_id BIGINT,
            scene_id BIGINT,
            object_id BIGINT,
            stats JSONB NOT NULL
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

print("CREATE TABLE script completed successfully")
