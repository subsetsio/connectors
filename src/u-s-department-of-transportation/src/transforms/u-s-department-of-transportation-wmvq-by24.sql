-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("terminal_id" AS BIGINT) AS terminal_id,
    "terminal_name",
    "term_city",
    "term_state",
    "term_country",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("census_year" AS BIGINT) AS census_year,
    CAST("data_year" AS BIGINT) AS data_year
FROM "u-s-department-of-transportation-wmvq-by24"
