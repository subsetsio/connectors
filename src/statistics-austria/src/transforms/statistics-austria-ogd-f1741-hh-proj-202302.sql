-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "province_nuts_2_digit_9",
    "private_households_at_the_end_of_the_year",
    "annual_average_of_private_households"
FROM "statistics-austria-ogd-f1741-hh-proj-202302"
