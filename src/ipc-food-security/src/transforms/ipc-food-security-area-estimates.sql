-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are sub-national area-period estimates and should not be summed with the national estimates table for the same analysis.
-- caution: Grouped analyses include a region group alongside areas; use group columns for grouping context, not as additional observations.
SELECT
    CAST("anl_id" AS BIGINT) AS anl_id,
    "country_code",
    "analysis_classification",
    "analysis_date",
    CAST("group_id" AS BIGINT) AS group_id,
    "group_name",
    CAST("aar_id" AS BIGINT) AS aar_id,
    "area",
    "period_code",
    "period_title",
    "period_from_date",
    "period_thru_date",
    "estimated_population",
    "census_population",
    "overall_phase_value",
    "overall_phase_label",
    "overall_trend",
    "classification_text",
    "hfa_population_percentage",
    "hfa_kcal_percentage",
    "hfa_significance_value",
    "hfa_significance_label",
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
FROM "ipc-food-security-area-estimates"
