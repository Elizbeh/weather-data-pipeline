
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
db_path = BASE_DIR / "data/weather.db"
json_path = BASE_DIR / "data/processed/weather_clean.json"

with json_path.open("r", encoding="utf-8") as file:
    readings = json.load(file)

connection = sqlite3.connect(db_path)

try:
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT NOT NULL UNIQUE,
            time TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            extracted_at TEXT,
            migrated_at TEXT
        )
    """)

    cursor.executemany("""
        INSERT OR IGNORE INTO weather_observations (
            source_id,
            time,
            temperature,
            humidity,
            wind_speed,
            extracted_at,
            migrated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            reading["source_id"],
            reading["time"],
            reading["temperature"],
            reading["humidity"],
            reading["wind_speed"],
            reading.get("extracted_at"),
            reading.get("migrated_at")
        )
        for reading in readings
    ])

    connection.commit()

    total = cursor.execute(
        "SELECT COUNT(*) FROM weather_observations"
    ).fetchone()[0]

    print(f"Processed {len(readings)} readings.")
    print(f"Total observations in database: {total}")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()
