{{ config(materialized='table') }}

select
    DATE(time) as observation_date,
    AVG(temperature) as avg_temperature,
    MIN(temperature) as min_temperature,
    MAX(temperature) as max_temperature,
    AVG(humidity) as avg_humidity
from {{ ref('stg_weather_observations') }}
group by DATE(time)