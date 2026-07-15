-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no._awarded" AS no_awarded
FROM "sg-data-d-acfa67acbec5995aae4b34356d008b81"
