-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "occurrence_of_long_term_health_problem",
    "indicator",
    "birth_cohort",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-shl030.px"
