-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_building",
    "indicator",
    "time_of_construction",
    "location",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rl21210.px"
