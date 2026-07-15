-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "BothHusbandandWifeWorking" AS bothhusbandandwifeworking,
    "OnlyHusbandWorking" AS onlyhusbandworking,
    "OnlyWifeWorking" AS onlywifeworking,
    "BothHusbandandWifeNotWorking" AS bothhusbandandwifenotworking
FROM "sg-data-d-b5eb4da16b8e854be95abbb36247f8ed"
