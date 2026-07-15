-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "race",
    "didnotparticipatepastyear",
    "inactive",
    "irregular",
    "regular"
FROM "sg-data-d-8873929ba66d131f5d49d85976abb964"
