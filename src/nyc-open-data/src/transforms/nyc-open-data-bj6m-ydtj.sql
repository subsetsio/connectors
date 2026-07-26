-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vendor",
    "waiver_partialfull",
    "percentage_original",
    "percentage_after_waiver",
    "contract_registration_date"
FROM "nyc-open-data-bj6m-ydtj"
