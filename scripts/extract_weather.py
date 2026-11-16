
import requests
import json
from pathlib import Path

url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&current=temperature_2m,relative_humidity_2m,wind_speed_10m"

try:
    # Fetch weather data from the API
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Extract current weather measurements
    new_reading = data["current"]

    # Define the file path
    file_path = Path("../data/raw/weather.json")

    # Ensure the directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Check whether the file already exists
    if file_path.exists():

        # Read existing weather data
        with file_path.open("r") as f:
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

    # Save all readings to the JSON file
    with file_path.open("w") as f:
        json.dump(existing_data, f, indent=4)

    print(f"Weather data successfully saved to {file_path}")

except requests.exceptions.RequestException as e:
    print("Error fetching weather data:", e)

except (OSError, json.JSONDecodeError, KeyError, ValueError) as e:
    print("Error processing weather data:", e)