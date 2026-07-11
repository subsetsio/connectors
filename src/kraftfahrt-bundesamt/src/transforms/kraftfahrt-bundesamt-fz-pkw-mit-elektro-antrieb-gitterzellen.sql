-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Berichtsjahr" AS BIGINT) AS berichtsjahr,
    "Gitterzelle" AS gitterzelle,
    "Anteil_Pkw_mit_Elektro_Antrieb" AS anteil_pkw_mit_elektro_antrieb,
    "ZS_Anteil_Pkw_mit_Elektro_Antri" AS zs_anteil_pkw_mit_elektro_antri,
    "ObjectId" AS objectid
FROM "kraftfahrt-bundesamt-fz-pkw-mit-elektro-antrieb-gitterzellen"
