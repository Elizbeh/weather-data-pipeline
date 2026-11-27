{{ config(materialized='table') }}

select
    source_id,
    time,
    temperature,
    humidity,
    wind_speed,
    extracted_at,
    migrated_at
from {{ source('weather', 'weather_observations') }}