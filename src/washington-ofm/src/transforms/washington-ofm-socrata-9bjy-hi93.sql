-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "county",
    CAST("to_sort_by_county_and_year" AS BIGINT) AS to_sort_by_county_and_year,
    CAST("to_sort_by_year_and_county" AS BIGINT) AS to_sort_by_year_and_county,
    CAST("year" AS BIGINT) AS year,
    "state_and_county_fips_code",
    CAST("beneficiaries_with_part_a_and_part_b" AS BIGINT) AS beneficiaries_with_part_a_and_part_b,
    CAST("ffs_beneficiaries" AS BIGINT) AS ffs_beneficiaries,
    CAST("ma_beneficiaries" AS BIGINT) AS ma_beneficiaries,
    CAST("ma_participation_rate" AS DOUBLE) AS ma_participation_rate,
    CAST("average_age" AS BIGINT) AS average_age,
    CAST("percent_female" AS DOUBLE) AS percent_female,
    CAST("percent_male" AS DOUBLE) AS percent_male,
    CAST("percent_non_hispanic_white" AS DOUBLE) AS percent_non_hispanic_white,
    CAST("percent_african_american" AS DOUBLE) AS percent_african_american,
    CAST("percent_hispanic" AS DOUBLE) AS percent_hispanic,
    CAST("percent_other_unknown" AS DOUBLE) AS percent_other_unknown,
    CAST("percent_eligible_for_medicaid" AS DOUBLE) AS percent_eligible_for_medicaid,
    CAST("average_hcc_score" AS DOUBLE) AS average_hcc_score
FROM "washington-ofm-socrata-9bjy-hi93"
