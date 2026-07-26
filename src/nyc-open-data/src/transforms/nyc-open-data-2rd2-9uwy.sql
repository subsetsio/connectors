-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "food_type",
    "from_new_york_state_source",
    "other_source_during_new_york_state_availability_period",
    "other_source_outside_new_york_state_availability_period"
FROM "nyc-open-data-2rd2-9uwy"
