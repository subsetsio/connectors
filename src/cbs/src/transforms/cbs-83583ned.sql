-- Banen van werknemers in december; economische activiteit (SBI 2008),
-- bedrijfsgrootte. Annual December measurement of employee jobs.
-- The table carries exactly one measure (M000308, "Banen van werknemers in
-- december", unit x 1 000) — the constant measure/unit columns are dropped
-- and documented on `jobs_thousands` instead. period_label arrives untrimmed.
SELECT
    "period"                                AS period,
    CAST(substr("period", 1, 4) AS BIGINT)  AS year,
    trim("period_label")                    AS period_label,
    "BedrijfstakkenBranchesSBI2008"         AS industry_sbi2008,
    "Bedrijfsgrootte"                       AS company_size,
    "value"                                 AS jobs_thousands
FROM "cbs-83583ned"
WHERE "value" IS NOT NULL
