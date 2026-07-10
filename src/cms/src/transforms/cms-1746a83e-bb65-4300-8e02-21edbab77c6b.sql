-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Suplr_NPI" AS BIGINT) AS suplr_npi,
    "Suplr_Prvdr_Last_Name_Org" AS suplr_prvdr_last_name_org,
    "Suplr_Prvdr_First_Name" AS suplr_prvdr_first_name,
    "Suplr_Prvdr_MI" AS suplr_prvdr_mi,
    "Suplr_Prvdr_Crdntls" AS suplr_prvdr_crdntls,
    "Suplr_Prvdr_Ent_Cd" AS suplr_prvdr_ent_cd,
    "Suplr_Prvdr_St1" AS suplr_prvdr_st1,
    "Suplr_Prvdr_St2" AS suplr_prvdr_st2,
    "Suplr_Prvdr_City" AS suplr_prvdr_city,
    "Suplr_Prvdr_State_Abrvtn" AS suplr_prvdr_state_abrvtn,
    CAST("Suplr_Prvdr_State_FIPS" AS BIGINT) AS suplr_prvdr_state_fips,
    CAST("Suplr_Prvdr_Zip5" AS BIGINT) AS suplr_prvdr_zip5,
    "Suplr_Prvdr_RUCA_Cat" AS suplr_prvdr_ruca_cat,
    "Suplr_Prvdr_RUCA" AS suplr_prvdr_ruca,
    "Suplr_Prvdr_RUCA_Desc" AS suplr_prvdr_ruca_desc,
    "Suplr_Prvdr_Cntry" AS suplr_prvdr_cntry,
    "Suplr_Prvdr_Spclty_Cd" AS suplr_prvdr_spclty_cd,
    "Suplr_Prvdr_Spclty_Desc" AS suplr_prvdr_spclty_desc,
    "Suplr_Prvdr_Spclty_Srce" AS suplr_prvdr_spclty_srce,
    "RBCS_Lvl" AS rbcs_lvl,
    "RBCS_Id" AS rbcs_id,
    "RBCS_Desc" AS rbcs_desc,
    "HCPCS_Cd" AS hcpcs_cd,
    "HCPCS_Desc" AS hcpcs_desc,
    "Suplr_Rentl_Ind" AS suplr_rentl_ind,
    "Tot_Suplr_Benes" AS tot_suplr_benes,
    CAST("Tot_Suplr_Clms" AS BIGINT) AS tot_suplr_clms,
    CAST("Tot_Suplr_Srvcs" AS BIGINT) AS tot_suplr_srvcs,
    CAST("Avg_Suplr_Sbmtd_Chrg" AS BIGINT) AS avg_suplr_sbmtd_chrg,
    CAST("Avg_Suplr_Mdcr_Alowd_Amt" AS DOUBLE) AS avg_suplr_mdcr_alowd_amt,
    CAST("Avg_Suplr_Mdcr_Pymt_Amt" AS DOUBLE) AS avg_suplr_mdcr_pymt_amt,
    CAST("Avg_Suplr_Mdcr_Stdzd_Amt" AS DOUBLE) AS avg_suplr_mdcr_stdzd_amt
FROM "cms-1746a83e-bb65-4300-8e02-21edbab77c6b"
