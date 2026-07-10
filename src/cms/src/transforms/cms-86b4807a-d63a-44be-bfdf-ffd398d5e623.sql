-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Rfrg_NPI" AS BIGINT) AS rfrg_npi,
    "Rfrg_Prvdr_Last_Name_Org" AS rfrg_prvdr_last_name_org,
    "Rfrg_Prvdr_First_Name" AS rfrg_prvdr_first_name,
    "Rfrg_Prvdr_MI" AS rfrg_prvdr_mi,
    "Rfrg_Prvdr_Crdntls" AS rfrg_prvdr_crdntls,
    "Rfrg_Prvdr_Ent_Cd" AS rfrg_prvdr_ent_cd,
    "Rfrg_Prvdr_St1" AS rfrg_prvdr_st1,
    "Rfrg_Prvdr_St2" AS rfrg_prvdr_st2,
    "Rfrg_Prvdr_City" AS rfrg_prvdr_city,
    "Rfrg_Prvdr_State_Abrvtn" AS rfrg_prvdr_state_abrvtn,
    "Rfrg_Prvdr_State_FIPS" AS rfrg_prvdr_state_fips,
    "Rfrg_Prvdr_Zip5" AS rfrg_prvdr_zip5,
    "Rfrg_Prvdr_RUCA_Cat" AS rfrg_prvdr_ruca_cat,
    "Rfrg_Prvdr_RUCA" AS rfrg_prvdr_ruca,
    "Rfrg_Prvdr_RUCA_Desc" AS rfrg_prvdr_ruca_desc,
    "Rfrg_Prvdr_Cntry" AS rfrg_prvdr_cntry,
    "Rfrg_Prvdr_Spclty_Cd" AS rfrg_prvdr_spclty_cd,
    "Rfrg_Prvdr_Spclty_Desc" AS rfrg_prvdr_spclty_desc,
    "Rfrg_Prvdr_Spclty_Srce" AS rfrg_prvdr_spclty_srce,
    "RBCS_Lvl" AS rbcs_lvl,
    "RBCS_Id" AS rbcs_id,
    "RBCS_Desc" AS rbcs_desc,
    "HCPCS_CD" AS hcpcs_cd,
    "HCPCS_Desc" AS hcpcs_desc,
    "Suplr_Rentl_Ind" AS suplr_rentl_ind,
    CAST("Tot_Suplrs" AS BIGINT) AS tot_suplrs,
    "Tot_Suplr_Benes" AS tot_suplr_benes,
    CAST("Tot_Suplr_Clms" AS BIGINT) AS tot_suplr_clms,
    CAST("Tot_Suplr_Srvcs" AS BIGINT) AS tot_suplr_srvcs,
    CAST("Avg_Suplr_Sbmtd_Chrg" AS DOUBLE) AS avg_suplr_sbmtd_chrg,
    CAST("Avg_Suplr_Mdcr_Alowd_Amt" AS DOUBLE) AS avg_suplr_mdcr_alowd_amt,
    CAST("Avg_Suplr_Mdcr_Pymt_Amt" AS DOUBLE) AS avg_suplr_mdcr_pymt_amt,
    CAST("Avg_Suplr_Mdcr_Stdzd_Amt" AS DOUBLE) AS avg_suplr_mdcr_stdzd_amt
FROM "cms-86b4807a-d63a-44be-bfdf-ffd398d5e623"
