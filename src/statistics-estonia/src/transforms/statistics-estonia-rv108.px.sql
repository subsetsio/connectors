-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "ethnic_nationality_of_mother",
    "ethnic_nationality_of_father",
    "value"
FROM "statistics-estonia-rv108.px"
