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
    "Unweighted Normalized Clinical Outcomes Domain Score" AS unweighted_normalized_clinical_outcomes_domain_score,
    "Weighted Normalized Clinical Outcomes Domain Score" AS weighted_normalized_clinical_outcomes_domain_score,
    "Unweighted Person And Community Engagement Domain Score" AS unweighted_person_and_community_engagement_domain_score,
    "Weighted Person And Community Engagement Domain Score" AS weighted_person_and_community_engagement_domain_score,
    "Unweighted Normalized Safety Domain Score" AS unweighted_normalized_safety_domain_score,
    "Weighted Safety Domain Score" AS weighted_safety_domain_score,
    "Unweighted Normalized Efficiency And Cost Reduction Domain Score" AS unweighted_normalized_efficiency_and_cost_reduction_domain_score,
    "Weighted Efficiency And Cost Reduction Domain Score" AS weighted_efficiency_and_cost_reduction_domain_score,
    CAST("Total Performance Score" AS DOUBLE) AS total_performance_score
FROM "cms-ypbt-wvdk"
