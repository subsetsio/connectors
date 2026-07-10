-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Facility Name" AS facility_name,
    "org_PAC_ID" AS org_pac_id,
    "ACO_ID_1" AS aco_id_1,
    "ACO_nm_1" AS aco_nm_1,
    "ACO_ID_2" AS aco_id_2,
    "ACO_nm_2" AS aco_nm_2,
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
FROM "cms-0ba7-2cb0"
