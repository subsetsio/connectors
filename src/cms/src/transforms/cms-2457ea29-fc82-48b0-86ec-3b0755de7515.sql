-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "MULTIPLE_NPI_FLAG" AS multiple_npi_flag,
    "PECOS_ASCT_CNTL_ID" AS pecos_asct_cntl_id,
    "ENRLMT_ID" AS enrlmt_id,
    "PROVIDER_TYPE_CD" AS provider_type_cd,
    "PROVIDER_TYPE_DESC" AS provider_type_desc,
    "STATE_CD" AS state_cd,
    "FIRST_NAME" AS first_name,
    "MDL_NAME" AS mdl_name,
    "LAST_NAME" AS last_name,
    "ORG_NAME" AS org_name
FROM "cms-2457ea29-fc82-48b0-86ec-3b0755de7515"
