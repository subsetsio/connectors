-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each analysis can contain up to three reporting periods; join to estimate tables and filter the period before comparing current and projected estimates.
SELECT
    CAST("anl_id" AS BIGINT) AS anl_id,
    "country_code",
    "classification",
    "title",
    "analysis_date",
    "fanalysis_date",
    "country_population",
    "public_map_link",
    "public_map_title",
    "has_groups",
    "period_count"
FROM "ipc-food-security-analyses"
