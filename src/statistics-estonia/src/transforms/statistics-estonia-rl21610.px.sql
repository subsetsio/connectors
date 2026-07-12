-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "extent_of_limitation",
    "occurrence_of_long_term_illness_or_health_problem",
    "place_of_residence",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rl21610.px"
