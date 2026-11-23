
-- =========================================
-- DATA QUALITY CHECKS
-- =========================================

-- 1. Check for missing required values
SELECT *
FROM weather_observations
WHERE source_id IS NULL
   OR time IS NULL
   OR temperature IS NULL
   OR humidity IS NULL
   OR wind_speed IS NULL;


-- 2. Check for invalid temperature values
-- Expected range: -50°C to 50°C
SELECT *
FROM weather_observations
WHERE temperature < -50
   OR temperature > 50;


-- 3. Check for duplicate source IDs
SELECT
    source_id,
    COUNT(*) AS occurrences
FROM weather_observations
GROUP BY source_id
HAVING COUNT(*) > 1;


-- 4. Check for invalid humidity values
-- Expected range: 0% to 100%
SELECT *
FROM weather_observations
WHERE humidity < 0
   OR humidity > 100;


-- 5. Check for negative wind speed
SELECT *
FROM weather_observations
WHERE wind_speed < 0;


-- 6. Check for duplicate timestamps
-- Multiple readings can share the same timestamp.
SELECT
    time,
    COUNT(*) AS total_records
FROM weather_observations
GROUP BY time
HAVING COUNT(*) > 1;


-- =========================================
-- WEATHER DATA ANALYSIS
-- =========================================

-- 7. Retrieve all weather observations
SELECT *
FROM weather_observations;


-- 8. Retrieve temperatures above 15 degrees
SELECT
    time,
    temperature
FROM weather_observations
WHERE temperature > 15;


-- 9. Sort observations from newest to oldest
SELECT *
FROM weather_observations
ORDER BY time DESC;


-- 10. Calculate average temperature
SELECT
    AVG(temperature) AS average_temperature
FROM weather_observations;


-- 11. Find the highest temperature
SELECT
    MAX(temperature) AS highest_temperature
FROM weather_observations;


SELECT
    DATE(time),
    AVG(temperature)
FROM weather_observations
GROUP BY DATE(time);

-- 12. Calculate daily average temperature
SELECT
    DATE(time) AS observation_date,
    AVG(temperature) AS average_temperature
FROM weather_observations
GROUP BY DATE(time)
ORDER BY observation_date;

SELECT
    DATE(time) AS observation_date,
    AVG(temperature) AS average_temperature,
    MIN(temperature) AS minimum_temperature,
    MAX(temperature) AS maximum_temperature
FROM weather_observations
GROUP BY DATE(time)
ORDER BY observation_date;