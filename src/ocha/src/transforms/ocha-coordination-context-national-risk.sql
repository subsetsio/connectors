-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is currently one national risk record per location; the reference_period_start column describes the index period rather than a row-level event date.
SELECT
    CAST("risk_class" AS BIGINT) AS risk_class,
    "global_rank",
    "overall_risk",
    "hazard_exposure_risk",
    "vulnerability_risk",
    "coping_capacity_risk",
    "meta_missing_indicators_pct",
    "meta_avg_recentness_years",
    "reference_period_start",
    CAST("reference_period_end" AS TIMESTAMP) AS reference_period_end,
    "resource_hdx_id",
    "location_code",
    "location_name"
FROM "ocha-coordination-context-national-risk"
