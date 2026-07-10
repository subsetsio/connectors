-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "Ind_PAC_ID" AS ind_pac_id,
    "Provider Last Name" AS provider_last_name,
    "Provider First Name" AS provider_first_name,
    "APM_affl_1" AS apm_affl_1,
    "APM_affl_2" AS apm_affl_2,
    "APM_affl_3" AS apm_affl_3,
    "APM_affl_4" AS apm_affl_4,
    "measure_cd",
    "measure_title",
    "invs_msr",
    "attestation_value",
    "prf_rate",
    "patient_count",
    "star_value",
    "five_star_benchmark",
    "collection_type",
    "CCXP_ind" AS ccxp_ind
FROM "cms-7d6a-e7a6"
