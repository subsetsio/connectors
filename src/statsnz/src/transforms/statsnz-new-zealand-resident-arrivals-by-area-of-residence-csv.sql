-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    strptime("year_month", '%Y-%m')::DATE AS year_month,
    "direction_code",
    "NZ_area" AS nz_area,
    CAST("Count" AS BIGINT) AS count,
    "geo_level",
    "period"
FROM "statsnz-new-zealand-resident-arrivals-by-area-of-residence-csv"
