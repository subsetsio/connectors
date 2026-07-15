-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "age",
    "labour_force",
    "employed",
    "unemployed",
    "outside_labour_force"
FROM "sg-data-d-a214d535743d69b51e95d2a4e6f3630e"
