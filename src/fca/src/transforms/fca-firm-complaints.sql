SELECT semester,
       breakdown_type,
       category,
       product,
       variable_type,
       variable,
       CAST(volume AS DOUBLE) AS volume
FROM "fca-firm-complaints"
WHERE volume IS NOT NULL AND semester IS NOT NULL
