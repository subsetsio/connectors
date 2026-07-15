-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "region",
    "export_revenue"
FROM "sg-data-d-3327d2bef55e24c8c84e1c1c4a992820"
