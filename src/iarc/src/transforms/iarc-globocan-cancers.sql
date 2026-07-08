SELECT
    CAST(cancer AS BIGINT)        AS cancer_code,
    CAST(label AS VARCHAR)        AS label,
    CAST(short_label AS VARCHAR)  AS short_label,
    CAST(ICD AS VARCHAR)          AS icd10,
    CAST(gender AS INTEGER)       AS gender,
    CAST(cancer_order AS INTEGER) AS cancer_order
FROM "iarc-globocan-cancers"
WHERE cancer IS NOT NULL
