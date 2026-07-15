-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "neonatal_mortality",
    "perinatal_mortality",
    "maternal_mortality"
FROM "sg-data-d-e4ce2fa3be49ca007ef72fbcefb997ef"
