-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "BothHusbandandWifeWorking" AS bothhusbandandwifeworking,
    "OnlyHusbandWorking" AS onlyhusbandworking,
    "OnlyWifeWorking" AS onlywifeworking,
    "BothHusbandandWifeNotWorking" AS bothhusbandandwifenotworking
FROM "sg-data-d-d9aecb2954fe4e5128985c7621091f59"
