-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name_of_foreign_architect",
    "company",
    "boa_registered_architect",
    "project_details",
    "project_period",
    "client",
    "submitted_on",
    "approved_on"
FROM "sg-data-d-521e0b73946484e83269d8ab4c7889cd"
