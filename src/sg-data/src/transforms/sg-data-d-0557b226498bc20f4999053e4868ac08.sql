-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "mother_race",
    "child_gender",
    "still_births_count"
FROM "sg-data-d-0557b226498bc20f4999053e4868ac08"
