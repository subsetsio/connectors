-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age",
    "labour_force",
    "employed",
    "unemployed",
    "outside_the_labour_force"
FROM "sg-data-d-12fc09011acb07b04aa484cbd5ea5ceb"
