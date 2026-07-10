-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "nuts2_regions",
    "age_of_mother",
    "age_specific_fertility_rate"
FROM "statistics-austria-ogd-ind002fertilrat-hvd-fertilrate-1"
