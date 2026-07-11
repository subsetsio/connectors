-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "month",
    "median",
    "lowerbound",
    "upperbound",
    "source",
    "notes",
    "publishdate"
FROM "guttmacher-institute-k4x7t"
