-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "awardNumber" AS awardnumber,
    "fiscalYear" AS fiscalyear,
    "programName" AS programname,
    "programAbbreviation" AS programabbreviation,
    "vendorState" AS vendorstate,
    "awardAmount" AS awardamount,
    "region",
    "vendorName" AS vendorname
FROM "fema-nondisasterassistancefirefightergrants"
