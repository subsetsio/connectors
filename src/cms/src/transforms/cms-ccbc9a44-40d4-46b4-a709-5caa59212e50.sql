-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Rndrng_Prvdr_CCN" AS rndrng_prvdr_ccn,
    "Rndrng_Prvdr_Org_Name" AS rndrng_prvdr_org_name,
    "Rndrng_Prvdr_St" AS rndrng_prvdr_st,
    "Rndrng_Prvdr_City" AS rndrng_prvdr_city,
    "Rndrng_Prvdr_State_Abrvtn" AS rndrng_prvdr_state_abrvtn,
    "Rndrng_Prvdr_State_FIPS" AS rndrng_prvdr_state_fips,
    "Rndrng_Prvdr_Zip5" AS rndrng_prvdr_zip5,
    CAST("Rndrng_Prvdr_RUCA" AS DOUBLE) AS rndrng_prvdr_ruca,
    "Rndrng_Prvdr_RUCA_Desc" AS rndrng_prvdr_ruca_desc,
    CAST("APC_Cd" AS BIGINT) AS apc_cd,
    "APC_Desc" AS apc_desc,
    "Bene_Cnt" AS bene_cnt,
    "CAPC_Srvcs" AS capc_srvcs,
    "Avg_Tot_Sbmtd_Chrgs" AS avg_tot_sbmtd_chrgs,
    "Avg_Mdcr_Alowd_Amt" AS avg_mdcr_alowd_amt,
    "Avg_Mdcr_Pymt_Amt" AS avg_mdcr_pymt_amt,
    "Outlier_Srvcs" AS outlier_srvcs,
    "Avg_Mdcr_Outlier_Amt" AS avg_mdcr_outlier_amt
FROM "cms-ccbc9a44-40d4-46b4-a709-5caa59212e50"
