-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "resource_id",
    "resource_name",
    "FinancialYear" AS financialyear,
    "HBT" AS hbt,
    "HBTQF" AS hbtqf,
    "Type" AS type,
    "Source" AS source,
    "Count" AS count
FROM "public-health-scotland-long-acting-reversible-methods-of-contraception-larc-in-scotland"
