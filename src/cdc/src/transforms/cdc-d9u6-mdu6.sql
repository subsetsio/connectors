-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Ferret" AS ferret,
    "Virus" AS virus,
    "HA" AS ha,
    "NA" AS na,
    CAST("HPAI" AS BOOLEAN) AS hpai,
    CAST("HPAI_MBAA" AS BOOLEAN) AS hpai_mbaa,
    "Origin" AS origin,
    "units",
    CAST("inoc_dose" AS DOUBLE) AS inoc_dose,
    CAST("NT" AS DOUBLE) AS nt,
    "Tr" AS tr,
    "Lg" AS lg,
    "BnOB" AS bnob,
    "Bn" AS bn,
    "Int" AS int
FROM "cdc-d9u6-mdu6"
