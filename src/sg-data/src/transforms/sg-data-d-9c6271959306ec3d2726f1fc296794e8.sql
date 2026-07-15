-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "sex",
    "occupation",
    "percentage"
FROM "sg-data-d-9c6271959306ec3d2726f1fc296794e8"
