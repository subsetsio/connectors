-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "vehicle_type",
    "average_annual_mileage"
FROM "sg-data-d-bdc4c6434e47b055de4b5f2fde10c1af"
