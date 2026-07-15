-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "hazardous_substances_licences_issued_annual",
    "hazardous_substances_permits_issued_annual"
FROM "sg-data-d-345313948f038e5aabc66ba33f4ea178"
