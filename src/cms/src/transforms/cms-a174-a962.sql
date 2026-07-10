-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "Org_PAC_ID" AS org_pac_id,
    "Provider Last Name" AS provider_last_name,
    "Provider First Name" AS provider_first_name,
    "source",
    "Facility-based scoring Certification number" AS facility_based_scoring_certification_number,
    "Facility Name" AS facility_name,
    "Quality_category_score" AS quality_category_score,
    "PI_category_score" AS pi_category_score,
    "IA_category_score" AS ia_category_score,
    "Cost_category_score" AS cost_category_score,
    "final_MIPS_score_without_CPB" AS final_mips_score_without_cpb,
    CAST("final_MIPS_score" AS DOUBLE) AS final_mips_score
FROM "cms-a174-a962"
