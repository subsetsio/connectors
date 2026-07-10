-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "health_care_providers_hp",
    "hf_1_government_schemes_and_compulsory_contributory_health_care_financing_schemes",
    "hf_1_1_government_schemes",
    "hf_1_2_compulsory_contributory_health_insurance_schemes",
    "hf_1_2_1_social_health_insurance_schemes",
    "hf_1_2_2_compulsory_private_insurance_schemes",
    "hf_2_voluntary_health_care_payment_schemes",
    "hf_2_1_voluntary_health_insurance_schemes",
    "hf_2_2_npish_financing_schemes",
    "hf_2_3_enterprise_financing_schemes",
    "hf_3_household_out_of_pocket_payment",
    "hf_3_1_out_of_pocket_excluding_cost_sharing",
    "hf_3_2_cost_sharing_with_third_party_payers",
    "hf_4_rest_of_the_world_financing_schemes_non_resident",
    "all_hf_all_financing_schemes"
FROM "statistics-austria-ogd-gesausgaben03-hvd-hphf-1"
