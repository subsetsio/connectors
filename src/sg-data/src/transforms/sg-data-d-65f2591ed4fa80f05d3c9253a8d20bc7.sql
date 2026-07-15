-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_organisation",
    "no._awarded" AS no_awarded
FROM "sg-data-d-65f2591ed4fa80f05d3c9253a8d20bc7"
