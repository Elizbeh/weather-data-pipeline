
from pathlib import Path
import json
import logging
from datetime import datetime, timezone
import hashlib


BASE_DIR = Path(__file__).resolve().parent.parent

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


file_path = BASE_DIR / "data/raw/weather.json"
transformed_file_path = BASE_DIR / "data/processed/weather_clean.json"

transformed_file_path.parent.mkdir(parents=True, exist_ok=True)

logger.info("Starting weather data transformation...")

try:
    with file_path.open("r", encoding="utf-8") as f:
        readings = json.load(f)

except (OSError, json.JSONDecodeError):
    logger.exception("Failed to read raw weather data.")
    raise

logger.info("Read %d raw weather readings.", len(readings))

            
transformed_data = []

invalid_count = 0

for index, reading in enumerate(readings):
    
    if (
        isinstance(reading.get("temperature_2m"), (int, float))
        and reading.get("time") is not None
        and isinstance(reading.get("relative_humidity_2m"), (int, float))
        and 0 <= reading["relative_humidity_2m"] <= 100
        and isinstance(reading.get("wind_speed_10m"), (int, float))
        and reading["wind_speed_10m"] >= 0
    ):
        source_data = json.dumps(reading, sort_keys=True)
        source_id = hashlib.sha256(
            f"{index}-{source_data}".encode("utf-8")
        ).hexdigest()

        new_reading = {
            "source_id": source_id,
            "time": reading["time"],
            "temperature": reading["temperature_2m"],
            "humidity": reading["relative_humidity_2m"],
            "wind_speed": reading["wind_speed_10m"],
            "extracted_at": reading.get("extracted_at"),
            "migrated_at": None
        }

        # Mark older readings without an extraction timestamp
        if new_reading["extracted_at"] is None:
            new_reading["migrated_at"] = datetime.now(
                timezone.utc
            ).isoformat()

        transformed_data.append(new_reading)

    else:
        invalid_count += 1
        logger.warning("Invalid weather reading skipped: %s", reading)

try:
    with transformed_file_path.open("w", encoding="utf-8") as file:
        json.dump(transformed_data, file, indent=4)

except OSError:
    logger.exception("Failed to save transformed weather data.")
    raise

logger.info("Valid readings: %d", len(transformed_data))
logger.info("Invalid readings skipped: %d", invalid_count)
logger.info("Transformed data saved to %s", transformed_file_path)
logger.info("Weather data transformation completed successfully.")