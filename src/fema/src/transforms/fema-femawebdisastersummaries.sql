-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "totalNumberIaApproved" AS totalnumberiaapproved,
    "totalAmountIhpApproved" AS totalamountihpapproved,
    "totalAmountHaApproved" AS totalamounthaapproved,
    "totalAmountOnaApproved" AS totalamountonaapproved,
    "totalObligatedAmountPa" AS totalobligatedamountpa,
    "totalObligatedAmountCatAb" AS totalobligatedamountcatab,
    "totalObligatedAmountCatC2g" AS totalobligatedamountcatc2g,
    "paLoadDate" AS paloaddate,
    "iaLoadDate" AS ialoaddate,
    "totalObligatedAmountHmgp" AS totalobligatedamounthmgp,
    "lastRefresh" AS lastrefresh,
    "hash"
FROM "fema-femawebdisastersummaries"
