
from pathlib import Path
import json

file_path = Path("../data/raw/weather.json")
transformed_file_path = Path("../data/processed/weather_clean.json")

# Ensure the output directory exists
transformed_file_path.parent.mkdir(parents=True, exist_ok=True)

with file_path.open("r") as f:
    readings = json.load(f)

transformed_data = []

for reading in readings:

    # Validate the weather reading
    if (
        isinstance(reading.get("temperature_2m"), (int, float))
        and reading.get("time") is not None
        and isinstance(reading.get("relative_humidity_2m"), (int, float))
        and 0 <= reading["relative_humidity_2m"] <= 100
        and isinstance(reading.get("wind_speed_10m"), (int, float))
        and reading["wind_speed_10m"] >= 0
    ):
        new_reading = {
            "time": reading["time"],
            "temperature": reading["temperature_2m"],
            "humidity": reading["relative_humidity_2m"],
            "wind_speed": reading["wind_speed_10m"]
        }

        transformed_data.append(new_reading)

    else:
        print("Invalid weather reading skipped:", reading)

# Save validated and transformed data
with transformed_file_path.open("w") as file:
    json.dump(transformed_data, file, indent=4)

print(f"Successfully saved {len(transformed_data)} valid readings to {transformed_file_path}")
