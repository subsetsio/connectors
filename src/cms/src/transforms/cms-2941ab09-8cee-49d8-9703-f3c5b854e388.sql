-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Rndrng_Prvdr_Geo_Lvl" AS rndrng_prvdr_geo_lvl,
    "Rndrng_Prvdr_Geo_Cd" AS rndrng_prvdr_geo_cd,
    "Rndrng_Prvdr_Geo_Desc" AS rndrng_prvdr_geo_desc,
    "DRG_Cd" AS drg_cd,
    "DRG_Desc" AS drg_desc,
    CAST("Tot_Dschrgs" AS BIGINT) AS tot_dschrgs,
    CAST("Avg_Submtd_Cvrd_Chrg" AS DOUBLE) AS avg_submtd_cvrd_chrg,
    CAST("Avg_Tot_Pymt_Amt" AS DOUBLE) AS avg_tot_pymt_amt,
    CAST("Avg_Mdcr_Pymt_Amt" AS DOUBLE) AS avg_mdcr_pymt_amt
FROM "cms-2941ab09-8cee-49d8-9703-f3c5b854e388"
