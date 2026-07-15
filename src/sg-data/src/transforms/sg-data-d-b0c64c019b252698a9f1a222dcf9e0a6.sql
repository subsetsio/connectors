-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "vessel_type",
    "number_of_vessels",
    "gross_tonnage"
FROM "sg-data-d-b0c64c019b252698a9f1a222dcf9e0a6"
