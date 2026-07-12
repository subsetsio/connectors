-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "full_part_time_job",
    "primary_activity",
    "sex",
    "period",
    "value"
FROM "statistics-estonia-ak033.px"
