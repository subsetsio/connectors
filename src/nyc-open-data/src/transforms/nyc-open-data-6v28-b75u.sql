-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "case_status",
    "allegations",
    "case_disposition",
    "case_count"
FROM "nyc-open-data-6v28-b75u"
