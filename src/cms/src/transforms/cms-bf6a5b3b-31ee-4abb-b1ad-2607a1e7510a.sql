-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Brnd_Name" AS brnd_name,
    "Gnrc_Name" AS gnrc_name,
    "HCPCS_Cd" AS hcpcs_cd,
    "HCPCS_Desc" AS hcpcs_desc,
    "Year" AS year,
    "Tot_Benes" AS tot_benes,
    CAST("Tot_Clms" AS BIGINT) AS tot_clms,
    CAST("Tot_Spndng" AS DOUBLE) AS tot_spndng,
    "Avg_Spnd_Per_Bene" AS avg_spnd_per_bene,
    CAST("Avg_Spnd_Per_Clm" AS DOUBLE) AS avg_spnd_per_clm
FROM "cms-bf6a5b3b-31ee-4abb-b1ad-2607a1e7510a"
