SELECT * EXCLUDE (obs_value),
       CAST(obs_value AS DOUBLE) AS obs_value
FROM "census-and-statistics-department-625-76102"
WHERE obs_value IS NOT NULL
