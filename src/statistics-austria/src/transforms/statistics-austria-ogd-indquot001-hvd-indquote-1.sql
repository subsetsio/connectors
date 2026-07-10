-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "nuts3_regions",
    "median_age_men_and_women_together",
    "median_age_of_men",
    "median_age_of_women"
FROM "statistics-austria-ogd-indquot001-hvd-indquote-1"
