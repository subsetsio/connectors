SELECT
    CAST(registry_code AS BIGINT) AS registry_code,
    CAST(registry AS VARCHAR)     AS registry,
    CAST(sex AS INTEGER)          AS sex,
    CAST(cancer_code AS BIGINT)   AS cancer_code,
    CAST(cancer AS VARCHAR)       AS cancer,
    CAST(icd10 AS VARCHAR)        AS icd10,
    CAST(age_band AS VARCHAR)     AS age_band,
    CAST(cases AS BIGINT)         AS cases
FROM "iarc-ci5-xii-summary"
WHERE registry_code IS NOT NULL
