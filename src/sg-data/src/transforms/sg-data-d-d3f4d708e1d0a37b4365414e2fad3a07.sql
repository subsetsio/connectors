-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "make",
    "importer_type",
    "fuel_type",
    "vehicle_type",
    "number"
FROM "sg-data-d-d3f4d708e1d0a37b4365414e2fad3a07"
