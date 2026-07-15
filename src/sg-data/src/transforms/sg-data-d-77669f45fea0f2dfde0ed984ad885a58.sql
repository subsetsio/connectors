-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "disciplines_of_study",
    "number"
FROM "sg-data-d-77669f45fea0f2dfde0ed984ad885a58"
