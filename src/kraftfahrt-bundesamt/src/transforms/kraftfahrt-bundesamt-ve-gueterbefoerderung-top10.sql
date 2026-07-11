-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Jahr" AS BIGINT) AS jahr,
    "Hauptverkehrsbeziehung" AS hauptverkehrsbeziehung,
    "Staaten" AS staaten,
    "Fahrten" AS fahrten,
    "ZS_Fahrten" AS zs_fahrten,
    "ObjectId" AS objectid
FROM "kraftfahrt-bundesamt-ve-gueterbefoerderung-top10"
