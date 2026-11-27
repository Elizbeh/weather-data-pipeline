{{ config(
    materialized='incremental',
    unique_key='source_id'
)}}

select
    source_id,
    time,
    temperature,
    humidity,
    wind_speed,
    extracted_at,
    migrated_at
from {{ source('weather', 'weather_observations') }} as source_data

{% if is_incremental() %}
    where not exists (
        select 1
        from {{ this }} as existing
        where existing.source_id = source_data.source_id
    )
{% endif %}