-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "level_of_school",
    "length_of_service",
    "no_of_vice_principals"
FROM "sg-data-d-afd4e884ea630562bed9e7048fa2b781"
