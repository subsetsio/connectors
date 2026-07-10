-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "city",
    "police_force_size",
    "all",
    "white",
    "non-white" AS non_white,
    "black",
    "hispanic",
    "asian"
FROM "fivethirtyeight-police-locals-police-locals"
