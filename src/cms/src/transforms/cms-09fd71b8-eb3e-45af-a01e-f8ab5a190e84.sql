-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "HCPCS_Cd" AS hcpcs_cd,
    "Brnd_Name" AS brnd_name,
    "Gnrc_Name" AS gnrc_name,
    CAST("Tot_Mdcr_Alowd_Amt" AS DOUBLE) AS tot_mdcr_alowd_amt,
    "Tot_Mdcr_Alowd_Admnrd_Amt" AS tot_mdcr_alowd_admnrd_amt,
    "Tot_Mdcr_Alowd_Dscrd_Amt" AS tot_mdcr_alowd_dscrd_amt,
    "PCT_Admnrd_Units" AS pct_admnrd_units,
    "PCT_Dscrd_Units" AS pct_dscrd_units
FROM "cms-09fd71b8-eb3e-45af-a01e-f8ab5a190e84"
