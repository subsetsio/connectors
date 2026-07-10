-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Rndrng_Prvdr_CCN" AS rndrng_prvdr_ccn,
    "Rndrng_Prvdr_Org_Name" AS rndrng_prvdr_org_name,
    "Rndrng_Prvdr_City" AS rndrng_prvdr_city,
    "Rndrng_Prvdr_St" AS rndrng_prvdr_st,
    "Rndrng_Prvdr_State_FIPS" AS rndrng_prvdr_state_fips,
    "Rndrng_Prvdr_Zip5" AS rndrng_prvdr_zip5,
    "Rndrng_Prvdr_State_Abrvtn" AS rndrng_prvdr_state_abrvtn,
    CAST("Rndrng_Prvdr_RUCA" AS DOUBLE) AS rndrng_prvdr_ruca,
    "Rndrng_Prvdr_RUCA_Desc" AS rndrng_prvdr_ruca_desc,
    "DRG_Cd" AS drg_cd,
    "DRG_Desc" AS drg_desc,
    CAST("Tot_Dschrgs" AS BIGINT) AS tot_dschrgs,
    CAST("Avg_Submtd_Cvrd_Chrg" AS DOUBLE) AS avg_submtd_cvrd_chrg,
    CAST("Avg_Tot_Pymt_Amt" AS DOUBLE) AS avg_tot_pymt_amt,
    CAST("Avg_Mdcr_Pymt_Amt" AS DOUBLE) AS avg_mdcr_pymt_amt
FROM "cms-690ddc6c-2767-4618-b277-420ffb2bf27c"
