-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "vessel_type",
    "number_of_vessels",
    "gross_tonnage"
FROM "sg-data-d-8f264219109e61fffa87ac64dd5a9a65"
