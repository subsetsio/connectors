-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "ethnic_group",
    "gender",
    "percentage"
FROM "sg-data-d-ec6b85ff143d7a62597fac7817ec3a67"
