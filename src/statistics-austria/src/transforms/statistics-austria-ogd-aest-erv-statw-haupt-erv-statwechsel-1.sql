-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "labour_market_status_before_the_status_change_level_3",
    "labour_market_status_after_the_status_change_level_3",
    "age_level_4",
    "sex",
    "number_of_status_changes"
FROM "statistics-austria-ogd-aest-erv-statw-haupt-erv-statwechsel-1"
