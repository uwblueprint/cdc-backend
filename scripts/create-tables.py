import psycopg2

hostname = "localhost"
database = "postgres_cdc_dev"
user = "postgres"
password = ""

conn = psycopg2.connect(host=hostname, database=database, user=user, password=password)

table_creation_commands = [
    """
        CREATE TABLE IF NOT EXISTS asset (
            id SERIAL PRIMARY KEY,
            name VARCHAR(256) NOT NULL,
            s3_key VARCHAR(256) NOT NULL,
            obj_type VARCHAR(50) NOT NULL
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS scenario (
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
        CREATE TABLE IF NOT EXISTS statistics (
            id SERIAL PRIMARY KEY,
            scenario_id BIGINT,
            scene_id BIGINT,
            object_id BIGINT,
            stats JSONB,
            FOREIGN KEY (scenario_id) REFERENCES scenario (id)
            --FOREIGN KEY (scene_id) REFERENCES (scene),
            --FOREIGN KEY (object_id) REFERENCES (object)
        )
    """,
]

cur = conn.cursor()

for command in table_creation_commands:
    cur.execute(command)

cur.close()
conn.commit()
