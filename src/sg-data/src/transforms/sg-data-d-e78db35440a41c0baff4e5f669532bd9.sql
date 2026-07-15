-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "arrival_passengers_count",
    "depart_passengers_count"
FROM "sg-data-d-e78db35440a41c0baff4e5f669532bd9"
