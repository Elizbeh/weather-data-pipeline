# Weather Data Pipeline

A Python-based data engineering project that extracts weather data from the Open-Meteo API, stores historical readings in JSON, and transforms raw data into a validated, structured dataset.

## Project Overview

This project demonstrates the fundamentals of building an ETL (Extract, Transform, Load) pipeline using Python.

The pipeline retrieves current weather information for Paris, France, stores the original API responses, and processes the collected readings into a clean dataset ready for further analysis.

The project focuses on data extraction, persistence, transformation, validation, and data quality.

## Architecture

```text
Open-Meteo API
      |
      v
Python Data Extraction
      |
      v
Raw JSON Storage
(data/raw/weather.json)
      |
      v
Data Transformation
      |
      v
Data Validation
      |
      v
Processed JSON Output
(data/processed/weather_clean.json)
```

## Technologies Used

- **Python** – data extraction, processing and validation.
- **Requests** – HTTP requests to the Open-Meteo API.
- **JSON** – raw and processed data storage.
- **Pathlib** – file and directory management.
- **Git & GitHub** – version control and source code management.
- **Linux (Ubuntu/WSL)** – development environment and command-line operations.

## Features

### 1. Data Extraction

- Retrieves current weather information from the Open-Meteo API.
- Uses HTTP requests with timeout handling.
- Handles unsuccessful HTTP responses and request exceptions.
- Extracts temperature, relative humidity, wind speed and measurement time.

### 2. Raw Data Storage

- Saves the original API data in JSON format.
- Maintains historical weather readings.
- Preserves the raw data separately from the processed dataset.

### 3. Data Transformation

- Extracts relevant fields from the raw weather readings.
- Renames fields for consistency:
  - `temperature_2m` → `temperature`
  - `relative_humidity_2m` → `humidity`
  - `wind_speed_10m` → `wind_speed`
- Produces a structured dataset.

### 4. Data Validation

The pipeline checks the quality of each reading before including it in the processed dataset.

Validation rules include:

- Temperature must be numeric.
- Measurement time must be present.
- Humidity must be between 0 and 100.
- Wind speed must be greater than or equal to zero.
- Invalid readings are excluded from the processed dataset.

## Project Structure

```text
weather-data-pipeline/
│
├── data/
│   ├── raw/
│   │   └── weather.json
│   │
│   └── processed/
│       └── weather_clean.json
│
├── scripts/
│   ├── extract_weather.py
│   └── transform_weather.py
│
├── .gitignore
└── README.md
```

**Note:** The data files are generated locally and excluded from Git using `.gitignore`.

## Getting Started

### Prerequisites

- Python 3
- pip
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Elizbeh/weather-data-pipeline.git
cd weather-data-pipeline
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install requests
```

### 4. Run the extraction script

```bash
cd scripts
python3 extract_weather.py
```

This retrieves weather data and saves the raw readings.

### 5. Run the transformation script

```bash
python3 transform_weather.py
```

This validates and transforms the raw readings before saving the cleaned dataset.

## Skills Demonstrated

Through this project, I have practised:

- Working with REST APIs and HTTP responses.
- Extracting and processing JSON data.
- Building a basic ETL workflow.
- Managing historical data.
- Implementing data validation and quality checks.
- Handling files and directories with Python.
- Using Git for version control.
- Working in a Linux development environment.

## Future Improvements

The project will be extended to explore additional data engineering technologies and practices:

- SQL database integration and analytical queries.
- dbt for data transformation and testing.
- BigQuery and Google Cloud Platform.
- Docker and Docker Compose.
- CI/CD automation using GitHub Actions.

## Data Source

Weather data is provided by the [Open-Meteo API](https://open-meteo.com/).

---

**Author:** Elizabeth Behaghel

**GitHub:** [github.com/Elizbeh](https://github.com/Elizbeh)

**Repository:** [weather-data-pipeline](https://github.com/Elizbeh/weather-data-pipeline)