-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are summary groups and country counts, not country-level observations; the sheet includes TI regions plus overall and 2025-only regime or civic-space groupings, so filter region before comparing groups across years.
SELECT
    "region",
    "year",
    "avg_cpi_score",
    "n"
FROM "transparency-international-cpi-regional-averages"
