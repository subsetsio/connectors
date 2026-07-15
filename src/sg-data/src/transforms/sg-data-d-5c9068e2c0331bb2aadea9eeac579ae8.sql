-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "incidence_of_retrenchment"
FROM "sg-data-d-5c9068e2c0331bb2aadea9eeac579ae8"
