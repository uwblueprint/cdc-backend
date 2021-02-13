import json
import os

from sqlalchemy import MetaData, create_engine

from app.config import config

hostname = config.get("postgres.hostname")
database = config.get("postgres.database")
user = config.get("postgres.user")
password = config.get("postgres.password", "")

tables = config.get("script.table-order")

path_to_json = "mockdata/"
db_url = "postgres://{user}:{password}@{hostname}/{database}".format(
    user=user, password=password, database=database, hostname=hostname
)
engine = create_engine(db_url)
meta = MetaData()
meta.reflect(bind=engine)
conn = engine.connect()
for table_name in tables:
    for file_name in [
        file
        for file in os.listdir(path_to_json)
        if file.startswith(table_name) and file.endswith(".json")
    ]:
        with open(path_to_json + file_name) as json_file:
            data = json.load(json_file)
            conn.execute(meta.tables[table_name].insert().values(data))
conn.close()
engine.dispose()

print("System's Data successfully loaded into Database!")
