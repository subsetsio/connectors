-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "_month" AS month,
    "currentyeartodate",
    "description",
    "actual",
    "plan"
FROM "nyc-open-data-g2t5-u7v8"
