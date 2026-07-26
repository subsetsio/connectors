-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "profile_id",
    "date",
    "total_charges",
    "export_date"
FROM "nyc-open-data-wq9a-qu9a"
