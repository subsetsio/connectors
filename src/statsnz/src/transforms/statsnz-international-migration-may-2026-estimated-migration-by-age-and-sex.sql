-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    strptime("year_month", '%Y-%m')::DATE AS year_month,
    strptime("month_of_release", '%Y-%m')::DATE AS month_of_release,
    "passenger_type",
    "direction",
    "sex",
    "age",
    CAST("estimate" AS BIGINT) AS estimate,
    CAST("standard_error" AS BIGINT) AS standard_error,
    "status"
FROM "statsnz-international-migration-may-2026-estimated-migration-by-age-and-sex"
