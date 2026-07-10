-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Rndrng_NPI" AS BIGINT) AS rndrng_npi,
    "Rndrng_Prvdr_Last_Org_Name" AS rndrng_prvdr_last_org_name,
    "Rndrng_Prvdr_First_Name" AS rndrng_prvdr_first_name,
    "Rndrng_Prvdr_MI" AS rndrng_prvdr_mi,
    "Rndrng_Prvdr_Crdntls" AS rndrng_prvdr_crdntls,
    "Rndrng_Prvdr_Ent_Cd" AS rndrng_prvdr_ent_cd,
    "Rndrng_Prvdr_St1" AS rndrng_prvdr_st1,
    "Rndrng_Prvdr_St2" AS rndrng_prvdr_st2,
    "Rndrng_Prvdr_City" AS rndrng_prvdr_city,
    "Rndrng_Prvdr_State_Abrvtn" AS rndrng_prvdr_state_abrvtn,
    "Rndrng_Prvdr_State_FIPS" AS rndrng_prvdr_state_fips,
    "Rndrng_Prvdr_Zip5" AS rndrng_prvdr_zip5,
    "Rndrng_Prvdr_RUCA" AS rndrng_prvdr_ruca,
    "Rndrng_Prvdr_RUCA_Desc" AS rndrng_prvdr_ruca_desc,
    "Rndrng_Prvdr_Cntry" AS rndrng_prvdr_cntry,
    "Rndrng_Prvdr_Type" AS rndrng_prvdr_type,
    "Rndrng_Prvdr_Mdcr_Prtcptg_Ind" AS rndrng_prvdr_mdcr_prtcptg_ind,
    "HCPCS_Cd" AS hcpcs_cd,
    "HCPCS_Desc" AS hcpcs_desc,
    "HCPCS_Drug_Ind" AS hcpcs_drug_ind,
    "Place_Of_Srvc" AS place_of_srvc,
    CAST("Tot_Benes" AS BIGINT) AS tot_benes,
    CAST("Tot_Srvcs" AS BIGINT) AS tot_srvcs,
    CAST("Tot_Bene_Day_Srvcs" AS BIGINT) AS tot_bene_day_srvcs,
    CAST("Avg_Sbmtd_Chrg" AS BIGINT) AS avg_sbmtd_chrg,
    CAST("Avg_Mdcr_Alowd_Amt" AS DOUBLE) AS avg_mdcr_alowd_amt,
    CAST("Avg_Mdcr_Pymt_Amt" AS DOUBLE) AS avg_mdcr_pymt_amt,
    CAST("Avg_Mdcr_Stdzd_Amt" AS DOUBLE) AS avg_mdcr_stdzd_amt
FROM "cms-92396110-2aed-4d63-a6a2-5d6207d46a29"
