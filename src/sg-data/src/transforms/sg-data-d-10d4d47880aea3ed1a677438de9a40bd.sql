-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "market_segment",
    "domestic_revenue"
FROM "sg-data-d-10d4d47880aea3ed1a677438de9a40bd"
