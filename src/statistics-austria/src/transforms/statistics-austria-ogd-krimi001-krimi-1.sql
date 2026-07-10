-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "district_of_higher_regional_court_and_regional_court_district_16",
    "number"
FROM "statistics-austria-ogd-krimi001-krimi-1"
