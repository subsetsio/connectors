SELECT
    CAST(observation_id AS BIGINT) AS observation_id,
    CAST(observation_date AS DATE) AS observation_date,
    CAST(EXTRACT(year FROM CAST(observation_date AS DATE)) AS INTEGER) AS year,
    CAST(species_id AS BIGINT) AS species_id,
    species_name,
    CAST(event_id AS BIGINT) AS event_id,
    event_name,
    CAST(latitude  AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude,
    CAST(recorder_id AS BIGINT) AS recorder_id
FROM "natures-calendar-observations"
WHERE observation_date IS NOT NULL
  AND observation_id IS NOT NULL
