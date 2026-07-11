-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source does not expose a stable natural key across the statistical dimensions in this layer; `ObjectId` is the ArcGIS row identifier.
SELECT
    "Berichtszeitpunkt" AS berichtszeitpunkt,
    "Hersteller" AS hersteller,
    "Handelsname" AS handelsname,
    "Typschluessel" AS typschluessel,
    "Bundesland" AS bundesland,
    "Anzahl" AS anzahl,
    "ZS_Anzahl" AS zs_anzahl,
    "ObjectId" AS objectid
FROM "kraftfahrt-bundesamt-fz-hersteller-handelsnamen-krad"
