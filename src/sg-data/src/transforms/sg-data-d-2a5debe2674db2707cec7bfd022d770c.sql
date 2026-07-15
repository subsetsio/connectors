-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "assault_rate_per_10000_inmates"
FROM "sg-data-d-2a5debe2674db2707cec7bfd022d770c"
