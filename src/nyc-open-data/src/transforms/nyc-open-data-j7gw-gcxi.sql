-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pin",
    "description",
    "selected_firm",
    "_value" AS value
FROM "nyc-open-data-j7gw-gcxi"
