-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ENRLMT_ID" AS enrlmt_id,
    "NPI" AS npi,
    "FIRST_NAME" AS first_name,
    "MDL_NAME" AS mdl_name,
    "LAST_NAME" AS last_name,
    "ORG_NAME" AS org_name,
    "MULTIPLE_NPI_FLAG" AS multiple_npi_flag,
    "STATE_CD" AS state_cd,
    "PROVIDER_TYPE_DESC" AS provider_type_desc,
    "REVOCATION_RSN" AS revocation_rsn,
    "REVOCATION_EFCTV_DT" AS revocation_efctv_dt,
    "REENROLLMENT_BAR_EXPRTN_DT" AS reenrollment_bar_exprtn_dt
FROM "cms-a6496a7d-4e19-479a-a9ad-d4c0a49e07c3"
