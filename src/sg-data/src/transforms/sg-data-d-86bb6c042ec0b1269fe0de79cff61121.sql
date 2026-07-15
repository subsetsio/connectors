-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "make",
    "fuel_type",
    "vehicle_type",
    "number"
FROM "sg-data-d-86bb6c042ec0b1269fe0de79cff61121"
