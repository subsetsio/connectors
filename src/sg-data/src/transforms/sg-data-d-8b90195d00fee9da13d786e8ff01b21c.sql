-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "WorkingStatusOfCouple_BothHusbandAndWifeWorking" AS workingstatusofcouple_bothhusbandandwifeworking,
    "WorkingStatusOfCouple_OnlyHusbandWorking" AS workingstatusofcouple_onlyhusbandworking,
    "WorkingStatusOfCouple_OnlyWifeWorking" AS workingstatusofcouple_onlywifeworking,
    "WorkingStatusOfCouple_BothHusbandAndWifeNotWorking" AS workingstatusofcouple_bothhusbandandwifenotworking
FROM "sg-data-d-8b90195d00fee9da13d786e8ff01b21c"
