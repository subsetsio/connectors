-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "period",
    "status",
    "sex",
    "age",
    CAST("population" AS BIGINT) AS population
FROM "statsnz-national-population-estimates-at-30-june-2018-population-by-sex-age-csv"
