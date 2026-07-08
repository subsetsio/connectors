SELECT
    TRY_CAST(activity_year AS INTEGER)    AS activity_year,
    TRY_CAST(calendar_quarter AS INTEGER) AS calendar_quarter,
    lei,
    tax_id,
    TRY_CAST(agency_code AS INTEGER)      AS agency_code,
    respondent_name,
    respondent_state,
    respondent_city,
    respondent_zip_code,
    TRY_CAST(lar_count AS BIGINT)         AS lar_count
FROM "ffiec-transmittal-sheet"
WHERE lei IS NOT NULL
  AND activity_year IS NOT NULL
-- one row per (filer, year); guard against any overlap across year batches
QUALIFY row_number() OVER (
    PARTITION BY lei, activity_year
    ORDER BY TRY_CAST(calendar_quarter AS INTEGER) DESC NULLS LAST
) = 1
