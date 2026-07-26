-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reporting_month",
    "data_month",
    "_program" AS program,
    "indicator",
    "indicator_subcategory",
    "count",
    "percentage",
    "dollars"
FROM "nyc-open-data-np6w-pies"
