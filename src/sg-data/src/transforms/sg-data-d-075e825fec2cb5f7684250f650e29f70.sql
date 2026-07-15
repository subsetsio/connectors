-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_organisations",
    "no._certified" AS no_certified
FROM "sg-data-d-075e825fec2cb5f7684250f650e29f70"
