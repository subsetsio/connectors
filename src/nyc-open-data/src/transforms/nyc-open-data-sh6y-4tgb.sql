-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "profile_id",
    "effective_date",
    "title",
    "shield_no",
    "export_date"
FROM "nyc-open-data-sh6y-4tgb"
