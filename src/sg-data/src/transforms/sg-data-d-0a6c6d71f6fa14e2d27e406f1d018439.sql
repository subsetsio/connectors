-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "town_estate",
    "number"
FROM "sg-data-d-0a6c6d71f6fa14e2d27e406f1d018439"
