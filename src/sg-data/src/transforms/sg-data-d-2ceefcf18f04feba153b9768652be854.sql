-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "actual_revised_estimated",
    "ministry",
    "number_archived",
    "number"
FROM "sg-data-d-2ceefcf18f04feba153b9768652be854"
