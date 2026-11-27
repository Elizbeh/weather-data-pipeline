{% snapshot weather_observations_snapshot %}

{{
    config(
        target_schema='main',
        unique_key='source_id',
        strategy='check',
        check_cols=['temperature', 'humidity', 'wind_speed']
    )
}}

SELECT
    source_id,
    time,
    temperature,
    humidity,
    wind_speed,
    extracted_at,
    migrated_at
FROM {{ source('weather', 'weather_observations') }}

{% endsnapshot %}