-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The sector domain includes both individual sectors and the Overall composite index; filter sector before aggregating across sectors.
SELECT
    "sector",
    "base_year",
    "date",
    "index_value",
    "growth_rate"
FROM "dpiit-core-industries"
