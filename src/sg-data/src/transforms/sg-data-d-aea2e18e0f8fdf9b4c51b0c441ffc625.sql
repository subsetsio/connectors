-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "domestic_waste_disposed"
FROM "sg-data-d-aea2e18e0f8fdf9b4c51b0c441ffc625"
