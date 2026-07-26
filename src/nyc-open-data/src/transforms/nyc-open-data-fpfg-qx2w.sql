-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "_month" AS month,
    "revenuesexpenditures",
    "description",
    "amount"
FROM "nyc-open-data-fpfg-qx2w"
