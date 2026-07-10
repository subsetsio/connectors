SELECT
    TRY_CAST(study_id AS INTEGER) AS study_id,
    NULLIF(citation_line, 'NA') AS citation_line
FROM "biotime-citations"
WHERE TRY_CAST(study_id AS INTEGER) IS NOT NULL
