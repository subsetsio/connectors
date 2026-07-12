-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_period",
    "full_part_time_job",
    "age_group",
    "sex",
    "indicator",
    "value"
FROM "statistics-estonia-tt0130.px"
