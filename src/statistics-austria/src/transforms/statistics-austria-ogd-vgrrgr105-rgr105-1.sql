-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "bundesland",
    "nace_2008",
    "change_in_to_previous_year_prices"
FROM "statistics-austria-ogd-vgrrgr105-rgr105-1"
