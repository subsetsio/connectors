-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "correspondence_between_educational_level_and_job_sought",
    "sex",
    "indicator",
    "value"
FROM "statistics-estonia-tt352.px"
