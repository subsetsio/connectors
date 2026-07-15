-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "housing_grant_scheme",
    "type_of_grant",
    "no_of_hh"
FROM "sg-data-d-a223380e5856cf06f7eac223e5902230"
