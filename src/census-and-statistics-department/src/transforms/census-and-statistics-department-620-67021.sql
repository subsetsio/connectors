SELECT * EXCLUDE (obs_value),
       CAST(obs_value AS DOUBLE) AS obs_value
FROM "census-and-statistics-department-620-67021"
WHERE obs_value IS NOT NULL
