-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "marital_status",
    "death_age_group",
    "gender",
    "death_count"
FROM "sg-data-d-0dd27335ae73fd0021c6025a2683a9de"
