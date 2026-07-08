SELECT * EXCLUDE (obs_value),
       CAST(obs_value AS DOUBLE) AS obs_value
FROM "census-and-statistics-department-315-37001"
WHERE obs_value IS NOT NULL
