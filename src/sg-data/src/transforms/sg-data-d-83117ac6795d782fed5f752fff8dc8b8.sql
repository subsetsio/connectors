-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "mother_age",
    "child_gender",
    "mother_race",
    "birth_count"
FROM "sg-data-d-83117ac6795d782fed5f752fff8dc8b8"
