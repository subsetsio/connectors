SELECT
    CAST(date AS DATE)        AS date,
    timestep                  AS frequency,
    aggregation,
    category,
    ner                       AS employment,
    ner_sa                    AS employment_sa
FROM "adp-ner-employment"
WHERE date IS NOT NULL
