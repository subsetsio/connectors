-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Fiscal Year" AS BIGINT) AS fiscal_year,
    "Facility ID" AS facility_id,
    "Facility Name" AS facility_name,
    "Address" AS address,
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "County/Parish" AS county_parish,
    CAST("MSPB-1 Achievement Threshold" AS DOUBLE) AS mspb_1_achievement_threshold,
    CAST("MSPB-1 Benchmark" AS DOUBLE) AS mspb_1_benchmark,
    "MSPB-1 Baseline Rate" AS mspb_1_baseline_rate,
    "MSPB-1 Performance Rate" AS mspb_1_performance_rate,
    "MSPB-1 Achievement Points" AS mspb_1_achievement_points,
    "MSPB-1 Improvement Points" AS mspb_1_improvement_points,
    "MSPB-1 Measure Score" AS mspb_1_measure_score
FROM "cms-su9h-3pvj"
