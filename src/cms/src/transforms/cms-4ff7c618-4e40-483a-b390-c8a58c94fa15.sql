-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Brnd_Name" AS brnd_name,
    "Gnrc_Name" AS gnrc_name,
    CAST("Tot_Mftr" AS BIGINT) AS tot_mftr,
    "Mftr_Name" AS mftr_name,
    "Year" AS year,
    "Tot_Benes" AS tot_benes,
    CAST("Tot_Clms" AS BIGINT) AS tot_clms,
    CAST("Tot_Spndng" AS DOUBLE) AS tot_spndng,
    "Avg_Spnd_Per_Bene" AS avg_spnd_per_bene,
    CAST("Avg_Spnd_Per_Clm" AS DOUBLE) AS avg_spnd_per_clm,
    "Drug_Uses" AS drug_uses
FROM "cms-4ff7c618-4e40-483a-b390-c8a58c94fa15"
