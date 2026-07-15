-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "residential_status",
    "ltu_rate"
FROM "sg-data-d-edc7e225d4e7c8f3532e6c329ba2bf79"
