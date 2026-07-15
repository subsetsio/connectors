-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "BothHusbandAndWifeWorking" AS bothhusbandandwifeworking,
    "OnlyHusbandWorking" AS onlyhusbandworking,
    "OnlyWifeWorking" AS onlywifeworking,
    "BothHusbandAndWifeNotWorking" AS bothhusbandandwifenotworking
FROM "sg-data-d-f68ef8a4ca30a26ca8444dbc6160a6da"
