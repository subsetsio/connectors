-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Berichtszeitpunkt" AS berichtszeitpunkt,
    "Herstellerschluessel" AS herstellerschluessel,
    "Herstellertext" AS herstellertext,
    "Typschluessel" AS typschluessel,
    "Handelsname" AS handelsname,
    "Anzahl" AS anzahl,
    "ZS_Anzahl" AS zs_anzahl,
    "ObjectId" AS objectid
FROM "kraftfahrt-bundesamt-fz-hersteller-handelsnamen-kfz"
