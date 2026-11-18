
from pathlib import Path
import json
from datetime import datetime, timezone
import hashlib


BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data/raw/weather.json"
transformed_file_path = BASE_DIR / "data/processed/weather_clean.json"

transformed_file_path.parent.mkdir(parents=True, exist_ok=True)

with file_path.open("r", encoding="utf-8") as f:
    readings = json.load(f)

transformed_data = []

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
        print("Invalid weather reading skipped:", reading)

with transformed_file_path.open("w", encoding="utf-8") as file:
    json.dump(transformed_data, file, indent=4)

print(f"Successfully saved {len(transformed_data)} valid readings.")
