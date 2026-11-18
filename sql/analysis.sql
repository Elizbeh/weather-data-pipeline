-- 1. Retrieve all weather observations

SELECT * FROM weather_observations;

SELECT
    time,
    COUNT(*) AS total_records
FROM weather_observations
GROUP BY time
HAVING COUNT(*) > 1;

-- 2. Retrieve temperatures above 15 degrees
SELECT time, temperature 
FROM weather_observations 
WHERE temperature > 15;

-- 3. Sort observations from newest to oldest
SELECT * FROM weather_observations
ORDER BY time DESC;

-- 4. Calculate average temperature
SELECT AVG(temperature)
AS average_temperature
FROM weather_observations;

-- 5. Find the highest temperature
SELECT MAX(temperature) 
AS highest_temperature
FROM weather_observations; 