-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "occurrence_of_long_term_illness_or_health_problem",
    CAST("year" AS BIGINT) AS year,
    "place_of_residence",
    "value"
FROM "statistics-estonia-rlv601.px"
