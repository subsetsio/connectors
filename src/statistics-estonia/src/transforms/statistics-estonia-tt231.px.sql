-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "distance_between_place_of_main_job_and_place_of_residence",
    "sex",
    "indicator",
    "value"
FROM "statistics-estonia-tt231.px"
