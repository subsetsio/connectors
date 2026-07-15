-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "occupation",
    "incidence_of_retrenchment"
FROM "sg-data-d-4a089fa8530d79b33766f85e48a68af5"
