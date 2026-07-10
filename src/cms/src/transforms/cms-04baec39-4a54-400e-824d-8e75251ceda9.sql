-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Rndrng_Prvdr_Geo_Lvl" AS rndrng_prvdr_geo_lvl,
    "Rndrng_Prvdr_Geo_Cd" AS rndrng_prvdr_geo_cd,
    "Rndrng_Prvdr_Geo_Desc" AS rndrng_prvdr_geo_desc,
    "Srvc_Lvl" AS srvc_lvl,
    CAST("APC_Cd" AS BIGINT) AS apc_cd,
    "APC_Desc" AS apc_desc,
    "HCPCS_Cd" AS hcpcs_cd,
    "HCPCS_Desc" AS hcpcs_desc,
    "Bene_Cnt" AS bene_cnt,
    "CAPC_Srvcs" AS capc_srvcs,
    "Avg_Tot_Sbmtd_Chrgs" AS avg_tot_sbmtd_chrgs,
    "Avg_Mdcr_Alowd_Amt" AS avg_mdcr_alowd_amt,
    "Avg_Mdcr_Pymt_Amt" AS avg_mdcr_pymt_amt,
    "Outlier_Srvcs" AS outlier_srvcs,
    "Avg_Mdcr_Outlier_Amt" AS avg_mdcr_outlier_amt
FROM "cms-04baec39-4a54-400e-824d-8e75251ceda9"
