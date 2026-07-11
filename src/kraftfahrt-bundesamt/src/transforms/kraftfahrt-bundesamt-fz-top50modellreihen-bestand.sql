-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Berichtszeitpunkt" AS berichtszeitpunkt,
    "Modellreihe" AS modellreihe,
    "Anzahl" AS anzahl,
    "ZS_Anzahl" AS zs_anzahl,
    "ObjectId" AS objectid
FROM "kraftfahrt-bundesamt-fz-top50modellreihen-bestand"
