import json
import psycopg2
import os

json_path = "/docker-entrypoint-initdb.d/cards.json"
ndjson_path = "/tmp/cards.ndjson"

print("Reading cards JSON...")
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Converting to NDJSON...")
with open(ndjson_path, "w", encoding="utf-8") as out:
    for obj in data:
        out.write(json.dumps(obj) + "\n")

print("Connecting to database...")
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB", "postgres"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD"),
    # host="localhost"
)
cur = conn.cursor()

print("Importing cards...")
with open(ndjson_path, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        id = obj.get("id")
        cur.execute(
            "INSERT INTO cards_raw (id, data) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (id, json.dumps(obj))
        )

conn.commit()
cur.close()
conn.close()
print("Done importing cards.")
