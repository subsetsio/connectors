-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "nuts_regions",
    CAST("age" AS BIGINT) AS age,
    "gender",
    "life_expectancy"
FROM "statistics-austria-ogd-ind003-hvd-ind-1"
