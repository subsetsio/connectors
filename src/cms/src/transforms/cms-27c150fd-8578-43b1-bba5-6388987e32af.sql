-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Rfrg_Prvdr_Geo_Lvl" AS rfrg_prvdr_geo_lvl,
    "Rfrg_Prvdr_Geo_Cd" AS rfrg_prvdr_geo_cd,
    "Rfrg_Prvdr_Geo_Desc" AS rfrg_prvdr_geo_desc,
    "RBCS_Lvl" AS rbcs_lvl,
    "RBCS_Id" AS rbcs_id,
    "RBCS_Desc" AS rbcs_desc,
    "HCPCS_Cd" AS hcpcs_cd,
    "HCPCS_Desc" AS hcpcs_desc,
    "Suplr_Rentl_Ind" AS suplr_rentl_ind,
    CAST("Tot_Rfrg_Prvdrs" AS BIGINT) AS tot_rfrg_prvdrs,
    CAST("Tot_Suplrs" AS BIGINT) AS tot_suplrs,
    "Tot_Suplr_Benes" AS tot_suplr_benes,
    CAST("Tot_Suplr_Clms" AS BIGINT) AS tot_suplr_clms,
    CAST("Tot_Suplr_Srvcs" AS BIGINT) AS tot_suplr_srvcs,
    CAST("Avg_Suplr_Sbmtd_Chrg" AS DOUBLE) AS avg_suplr_sbmtd_chrg,
    CAST("Avg_Suplr_Mdcr_Alowd_Amt" AS DOUBLE) AS avg_suplr_mdcr_alowd_amt,
    CAST("Avg_Suplr_Mdcr_Pymt_Amt" AS DOUBLE) AS avg_suplr_mdcr_pymt_amt,
    CAST("Avg_Suplr_Mdcr_Stdzd_Amt" AS DOUBLE) AS avg_suplr_mdcr_stdzd_amt
FROM "cms-27c150fd-8578-43b1-bba5-6388987e32af"
