-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Rndrng_Prvdr_Geo_Lvl" AS rndrng_prvdr_geo_lvl,
    "Rndrng_Prvdr_Geo_Cd" AS rndrng_prvdr_geo_cd,
    "Rndrng_Prvdr_Geo_Desc" AS rndrng_prvdr_geo_desc,
    "HCPCS_Cd" AS hcpcs_cd,
    "HCPCS_Desc" AS hcpcs_desc,
    "HCPCS_Drug_Ind" AS hcpcs_drug_ind,
    "Place_Of_Srvc" AS place_of_srvc,
    CAST("Tot_Rndrng_Prvdrs" AS BIGINT) AS tot_rndrng_prvdrs,
    CAST("Tot_Benes" AS BIGINT) AS tot_benes,
    CAST("Tot_Srvcs" AS BIGINT) AS tot_srvcs,
    CAST("Tot_Bene_Day_Srvcs" AS BIGINT) AS tot_bene_day_srvcs,
    CAST("Avg_Sbmtd_Chrg" AS DOUBLE) AS avg_sbmtd_chrg,
    CAST("Avg_Mdcr_Alowd_Amt" AS DOUBLE) AS avg_mdcr_alowd_amt,
    CAST("Avg_Mdcr_Pymt_Amt" AS DOUBLE) AS avg_mdcr_pymt_amt,
    CAST("Avg_Mdcr_Stdzd_Amt" AS DOUBLE) AS avg_mdcr_stdzd_amt
FROM "cms-6fea9d79-0129-4e4c-b1b8-23cd86a4f435"
