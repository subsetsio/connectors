-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are national totals by analysis period and should not be summed with sub-national area estimates for the same analysis.
-- caution: Phase 3+ is a cumulative severity measure that includes phases 3, 4, and 5; do not add it to the individual phase columns.
SELECT
    CAST("anl_id" AS BIGINT) AS anl_id,
    "country_code",
    "classification",
    "period_code",
    "period_name",
    "period_type",
    "period_from_date",
    "period_thru_date",
    "analysis_date",
    "analyzed_population",
    "phase1_population",
    "phase1_percentage",
    "phase2_population",
    "phase2_percentage",
    "phase3_population",
    "phase3_percentage",
    "phase4_population",
    "phase4_percentage",
    "phase5_population",
    "phase5_percentage",
    "phase3_plus_population",
    "phase3_plus_percentage"
FROM "ipc-food-security-national-estimates"
