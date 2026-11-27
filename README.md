# Weather Data Pipeline

A Python-based Data Engineering project that extracts weather data from the Open-Meteo API, transforms and validates it, and loads historical observations into a SQLite database for analysis.

The project also uses **dbt (Data Build Tool)** to transform structured data, implement data quality tests, generate documentation, perform incremental transformations and track historical changes using snapshots.

## Project Overview

This project demonstrates the fundamentals of building an end-to-end Data Engineering pipeline.

The Python ETL pipeline retrieves current weather information for Paris, France, stores raw API responses in JSON format, transforms and validates collected readings, and loads them into a SQLite database.

The dbt layer builds on this data by providing structured SQL transformations, data quality testing, incremental models, historical tracking and data documentation.

The project currently uses local tools and a SQLite database, keeping development costs at zero.

## Architecture

```text
              Open-Meteo API
                     |
                     v
            Data Extraction
                 (Python)
                     |
                     v
              Raw JSON Storage
                     |
                     v
           Data Transformation
                     |
                     v
              Data Validation
                     |
                     v
             Processed JSON
                     |
                     v
              SQLite Database
              (weather.db)
                     |
                     v
             dbt Transformations
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Staging   Incremental   Snapshots
        Models     Models      (History)
          |          |          |
          +----------+----------+
                     |
                     v
           Daily Weather Summary
                     |
                     v
          dbt Data Quality Tests
                     |
                     v
           dbt Documentation
```

## Technologies Used

- **Python** – data extraction, transformation and loading.
- **Requests** – HTTP requests to the Open-Meteo API.
- **JSON** – raw and processed data storage.
- **SQLite** – structured storage of weather observations.
- **SQL** – data transformations, quality checks and analysis.
- **dbt Core** – SQL-based data transformation, testing, documentation and snapshots.
- **dbt-sqlite** – SQLite adapter for dbt.
- **SQLean (crypto extension)** – provides the MD5 functionality required by dbt snapshots.
- **Logging** – pipeline execution monitoring and error tracking.
- **Pathlib** – file and directory management.
- **Hashlib (SHA-256)** – generating unique identifiers for source records.
- **Git & GitHub** – version control and source code management.
- **Linux (Ubuntu/WSL2)** – development environment.

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
- Preserves extraction timestamps and records migration timestamps.
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

### 7. Logging and Pipeline Monitoring

- Implements Python's built-in `logging` module across the extraction, transformation and loading scripts.
- Records pipeline execution events and processing information.
- Logs successful operations, processed record counts and database loading results.
- Captures errors and exception tracebacks to support troubleshooting.
- Writes logs to both the terminal and a persistent log file.

### 8. SQL Data Quality Checks and Analysis

Implements SQL queries to monitor data quality and explore stored weather observations.

Data quality checks include:

- Identifying missing required values.
- Detecting temperatures outside the expected range.
- Checking for duplicate `source_id` values.
- Identifying humidity values outside the 0–100% range.
- Detecting negative wind speeds.
- Identifying duplicate measurement timestamps.

Data analysis includes:

- Selecting and filtering records.
- Sorting observations by measurement time.
- Calculating overall average and maximum temperatures.
- Grouping observations by date.
- Calculating daily average, minimum and maximum temperatures.

## dbt Transformation and Analytics

The project uses dbt Core with the SQLite adapter to build and manage SQL transformations on top of the existing weather database.

### 1. Staging Models

Created staging models to prepare source data for downstream transformations.

- `stg_weather_observations`: selects and structures weather observations from the source table.
- Uses dbt's `source()` function to reference the original SQLite table.
- Uses dbt's `ref()` function to manage dependencies between models.

### 2. Analytical Models

Created `daily_weather_summary` to aggregate weather observations by calendar date.

The model calculates:

- Daily average temperature.
- Daily minimum temperature.
- Daily maximum temperature.
- Daily average humidity.

### 3. Incremental Models

Implemented `int_weather_incremental` using dbt's incremental materialization.

- Uses `source_id` as the unique identifier.
- Uses a `NOT EXISTS` condition to identify records not already present in the target table.
- Processes new observations without reloading existing records.
- Prevents duplicate records during repeated executions.

The incremental model was tested by adding three new source records and verifying that the target table increased from 17 to 20 records.

A subsequent execution confirmed that the row count remained at 20.

### 4. Data Quality Testing with dbt

Implemented dbt data tests to validate source data and transformed models.

Tests include:

- `not_null` checks on required fields.
- `unique` checks on `source_id`.
- Uniqueness and non-null checks on daily observation dates.
- Validation of important analytical fields.

Successfully executed dbt tests on the source, staging and analytical models.

### 5. Historical Tracking with dbt Snapshots

Implemented a dbt snapshot using the `check` strategy to track changes in weather observations.

The snapshot monitors:

- `temperature`
- `humidity`
- `wind_speed`

Uses `source_id` as the unique key to identify individual observations.

The snapshot implements Slowly Changing Dimension (SCD) Type 2 behaviour by preserving previous versions of records when monitored values change.

Historical tracking columns include:

- `dbt_scd_id`
- `dbt_updated_at`
- `dbt_valid_from`
- `dbt_valid_to`

Tested the snapshot by changing a synthetic weather observation from 10°C to 14°C.

Verified that dbt preserved the original version, closed its validity period and created a new active version.

### 6. dbt Documentation and Lineage

- Generated dbt project documentation using `dbt docs generate`.
- Explored model documentation and the lineage graph.
- Used dbt documentation to understand model dependencies and data flow.

## Project Structure

```text
weather-data-pipeline/
├── data/
│   ├── raw/
│   │   └── weather.json
│   ├── processed/
│   │   └── weather_clean.json
│   └── weather.db
├── scripts/
│   ├── extract_weather.py
│   ├── transform_weather.py
│   ├── load_weather.py
│   └── query_weather.py
├── sql/
│   └── analysis.sql
├── logs/
│   └── pipeline.log
├── weather_dbt/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_weather_observations.sql
│   │   │   ├── daily_weather_summary.sql
│   │   │   └── int_weather_incremental.sql
│   │   └── example/
│   ├── snapshots/
│   │   └── weather_observations_snapshot.sql
│   ├── tests/
│   ├── analyses/
│   ├── macros/
│   ├── dbt_project.yml
│   └── README.md
├── .gitignore
└── README.md
```

**Note:** Data files, SQLite databases, local backups, generated documentation and logs are managed locally and excluded from Git where appropriate. The dbt profile is configured separately in `~/.dbt/profiles.yml`.

## Getting Started

### Prerequisites

- Python 3
- pip
- Git
- SQLite3
- Linux or WSL2

### 1. Clone the repository

```bash
git clone https://github.com/Elizbeh/weather-data-pipeline.git
cd weather-data-pipeline
```

### 2. Create and activate the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

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

**Run SQL data quality checks and analysis:**

```bash
python3 scripts/query_weather.py
```

### 5. Set up dbt

The dbt environment is maintained separately from the original Python environment.

Install Python 3.11 and create a virtual environment:

```bash
uv python install 3.11
uv venv .venv-dbt --python 3.11
source .venv-dbt/bin/activate
```

Install dbt and the SQLite adapter:

```bash
uv pip install "dbt-core>=1.10,<1.11" "dbt-sqlite==1.10.0"
```

Configure the SQLite connection in `~/.dbt/profiles.yml` to point to the local `data/weather.db` database.

The SQLite `crypto` extension from SQLean is also required for the MD5 functionality used by dbt snapshots.

### 6. Run dbt transformations and tests

Validate the project:

```bash
dbt debug --project-dir weather_dbt
dbt parse --project-dir weather_dbt
```

Run the models:

```bash
dbt run --project-dir weather_dbt
```

Execute data quality tests:

```bash
dbt test --project-dir weather_dbt
```

Execute snapshots:

```bash
dbt snapshot --project-dir weather_dbt
```

Generate and serve documentation:

```bash
dbt docs generate --project-dir weather_dbt
dbt docs serve --project-dir weather_dbt
```

## Skills Demonstrated

Through this project, I have practised:

- Building an ETL pipeline with Python.
- Working with REST APIs and HTTP responses.
- Extracting and processing JSON data.
- Implementing data validation and quality checks.
- Managing historical datasets.
- Working with relational databases and SQLite.
- Writing SQL queries for data analysis and aggregation.
- Implementing incremental data loading.
- Preventing duplicate records using unique identifiers.
- Using dbt for SQL-based data transformations.
- Creating staging and analytical models.
- Implementing dbt data tests.
- Tracking historical changes using dbt snapshots and SCD Type 2.
- Generating data documentation and understanding model lineage.
- Implementing application logging and error handling.
- Monitoring pipeline execution.
- Managing files and directories with Python.
- Using Git and Linux command-line tools.

## Future Improvements

The project will be extended to explore additional Data Engineering technologies and practices:

- **BigQuery** for cloud data warehousing.
- **Google Cloud Platform** integration.
- **Docker and Docker Compose** for containerisation.
- **CI/CD automation** using GitHub Actions.
- Automated pipeline scheduling and orchestration.
- Additional data quality and monitoring capabilities.

## Data Source

Weather data is provided by the [Open-Meteo API](https://open-meteo.com/).

---

**Author:** Elizabeth Behaghel

**GitHub:** [github.com/Elizbeh](https://github.com/Elizbeh)

**Repository:** [weather-data-pipeline](https://github.com/Elizbeh/weather-data-pipeline)
