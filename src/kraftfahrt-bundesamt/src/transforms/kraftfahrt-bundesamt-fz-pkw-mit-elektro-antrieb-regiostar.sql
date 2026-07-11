-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Berichtszeitpunkt" AS DOUBLE) AS berichtszeitpunkt,
    "RegioStaR7" AS regiostar7,
    "Pkw_Elektro_Anteil" AS pkw_elektro_anteil,
    "ZS_Pkw_Elektro_Anteil" AS zs_pkw_elektro_anteil,
    "OBJECTID" AS objectid,
    "Regiostar7_Nummer" AS regiostar7_nummer
FROM "kraftfahrt-bundesamt-fz-pkw-mit-elektro-antrieb-regiostar"
