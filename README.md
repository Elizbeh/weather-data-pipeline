# Weather Data Pipeline

A Python-based Data Engineering project that extracts weather data from the Open-Meteo API, transforms and validates it, and loads historical observations into a SQLite database for analysis.

## Project Overview

This project demonstrates the fundamentals of building an ETL (Extract, Transform, Load) pipeline using Python.

The pipeline retrieves current weather information for Paris, France, stores raw API responses in JSON format, transforms and validates the collected readings, and loads them into a SQLite database.

It also implements incremental data loading to preserve historical observations and prevent duplicate records.

## Architecture

```text
Open-Meteo API
      |
      v
Data Extraction (Python)
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
Processed JSON
(data/processed/weather_clean.json)
      |
      v
SQLite Database
(data/weather.db)
      |
      v
SQL Analysis
(sql/analysis.sql)
```

## Technologies Used

- **Python** – data extraction, transformation and loading.
- **Requests** – HTTP requests to the Open-Meteo API.
- **JSON** – raw and processed data storage.
- **SQLite** – structured storage of historical weather observations.
- **SQL** – querying and analysing weather data.
- **Pathlib** – file and directory management.
- **Hashlib (SHA-256)** – generating unique identifiers for source records.
- **Git & GitHub** – version control and source code management.
- **Linux (Ubuntu/WSL)** – development environment.

## Features

### 1. Data Extraction

- Retrieves current weather information from the Open-Meteo API.
- Uses HTTP requests with timeout handling.
- Handles unsuccessful HTTP responses and request exceptions.
- Extracts temperature, relative humidity, wind speed and measurement time.
- Records extraction timestamps to distinguish measurement time from extraction time.

### 2. Raw Data Storage

- Saves original API readings in JSON format.
- Maintains historical weather readings.
- Preserves raw data separately from the processed dataset.

### 3. Data Transformation

- Extracts relevant fields from raw weather readings.
- Renames fields for consistency:
  - `temperature_2m` → `temperature`
  - `relative_humidity_2m` → `humidity`
  - `wind_speed_10m` → `wind_speed`
- Generates a unique `source_id` using SHA-256.
- Preserves extraction timestamps and records migration timestamps for older readings.
- Produces a structured dataset in JSON format.

### 4. Data Validation

The pipeline checks the quality of each reading before including it in the processed dataset.

Validation rules include:

- Temperature must be numeric.
- Measurement time must be present.
- Humidity must be between 0 and 100.
- Wind speed must be numeric and greater than or equal to zero.
- Invalid readings are excluded from the processed dataset.

### 5. SQLite Database Integration

- Loads validated weather observations into a SQLite database.
- Uses an auto-incrementing primary key for database records.
- Uses `source_id` as a unique identifier.
- Preserves multiple observations even when their measurement timestamps are identical.
- Stores extraction and migration timestamps.

### 6. Incremental Data Loading

- Implements `INSERT OR IGNORE` to prevent duplicate records.
- Uses a unique constraint on `source_id`.
- Inserts new observations without deleting existing historical data.
- Allows the loader to be executed repeatedly without duplicating previously loaded records.

### 7. SQL Analysis

Uses SQL queries to explore stored weather observations, including:

- Selecting and filtering records.
- Sorting observations.
- Calculating average, minimum and maximum temperatures.
- Identifying duplicate measurement timestamps.
- Grouping observations by date.

## Project Structure

```text
weather-data-pipeline/
├── data/
│   ├── raw/
│   │   └── weather.json
│   ├── processed/
│   │   └── weather_clean.json
│   ├── weather.db
│   └── weather_backup.db
├── scripts/
│   ├── extract_weather.py
│   ├── transform_weather.py
│   ├── load_weather.py
│   └── query_weather.py
├── sql/
│   └── analysis.sql
├── .gitignore
└── README.md
```

**Note:** Data files, SQLite databases and local backups are generated locally and excluded from Git using `.gitignore`.

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

### 4. Run the ETL pipeline

Execute the scripts from the project root directory.

**Extract weather data:**

```bash
python3 scripts/extract_weather.py
```

**Transform and validate the data:**

```bash
python3 scripts/transform_weather.py
```

**Load data into SQLite:**

```bash
python3 scripts/load_weather.py
```

**Run SQL analysis queries:**

```bash
python3 scripts/query_weather.py
```

## Skills Demonstrated

Through this project, I have practised:

- Building an ETL pipeline with Python.
- Working with REST APIs and HTTP responses.
- Extracting and processing JSON data.
- Implementing data validation and quality checks.
- Managing historical datasets.
- Working with relational databases and SQLite.
- Writing SQL queries for data analysis.
- Implementing incremental data loading.
- Preventing duplicate records using unique identifiers.
- Managing files and directories with Python.
- Using Git and Linux command-line tools.

## Future Improvements

The project will be extended to explore additional Data Engineering technologies and practices:

- dbt for data transformation, testing and documentation.
- BigQuery for cloud data warehousing.
- Google Cloud Platform integration.
- Docker and Docker Compose.
- CI/CD automation using GitHub Actions.
- Automated data quality testing and logging.

## Data Source

Weather data is provided by the [Open-Meteo API](https://open-meteo.com/).

---

**Author:** Elizabeth Behaghel

**GitHub:** [github.com/Elizbeh](https://github.com/Elizbeh)

**Repository:** [weather-data-pipeline](https://github.com/Elizbeh/weather-data-pipeline)