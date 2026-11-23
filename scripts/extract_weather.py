
import requests
import json
import logging
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    handlers = [
        logging.FileHandler(
            BASE_DIR / "logs/pipeline.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger =  logging.getLogger(__name__)

url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&current=temperature_2m,relative_humidity_2m,wind_speed_10m"

try:
    logger.info("Starting weather data extraction...")
    logger.info("Sending request to Open-Meteo API...")

    # Fetch weather data from the API
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    logger.info("API request successful.")
    data = response.json()

    # Extract current weather measurements
    new_reading = data["current"].copy()

    # Record the actual extraction timestamp
    new_reading["extracted_at"] = datetime.now(timezone.utc).isoformat()
    
    logger.info("Weather reading extracted successfully.")

    # Define the file path
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data/raw/weather.json"  

    # Ensure the directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Check whether the file already exists
    if file_path.exists():

        # Read existing weather data
        with file_path.open("r", encoding="utf-8") as f:
            json_data = json.load(f)

        # Convert the original dictionary into a list
        if isinstance(json_data, dict):
            existing_data = [json_data["current"]]

        # Preserve existing readings if already a list
        elif isinstance(json_data, list):
            existing_data = json_data

        else:
            raise ValueError("Unexpected JSON data format")

    else:
        # Start with an empty list if the file doesn't exist
        existing_data = []

    # Add the new weather reading
    existing_data.append(new_reading)
    
    logger.info("Total readings in raw data: %d", len(existing_data))

    # Save all readings to the JSON file
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4)

    logger.info("Weather data successfully saved to %s", file_path)
    
except requests.exceptions.RequestException as e:
    logger.exception("Error fetching weather data:", e)

except (OSError, json.JSONDecodeError, KeyError, ValueError) as e:
    logger.exception("Error processing weather data:", e)   