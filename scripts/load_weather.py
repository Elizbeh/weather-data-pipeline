
import sqlite3
import json
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(
            BASE_DIR / "logs/pipeline.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
db_path = BASE_DIR / "data/weather.db"
json_path = BASE_DIR / "data/processed/weather_clean.json"

connection = None

try:
    logger.info("Starting data loading...")

    with json_path.open("r", encoding="utf-8") as file:
        readings = json.load(file)

    logger.info("Read %d readings from processed JSON.", len(readings))

    connection = sqlite3.connect(db_path)
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

    inserted = cursor.rowcount
    skipped = len(readings) - inserted

    connection.commit()

    total = cursor.execute(
        "SELECT COUNT(*) FROM weather_observations"
    ).fetchone()[0]

    logger.info("Processed: %d readings.", len(readings))
    logger.info("New records inserted: %d.", inserted)
    logger.info("Duplicate records skipped: %d.", skipped)
    logger.info("Total observations in database: %d.", total)
    logger.info("Data loading completed successfully.")

except Exception:
    if connection is not None:
        connection.rollback()

    logger.exception("Data loading failed.")
    raise

finally:
    if connection is not None:
        connection.close()
