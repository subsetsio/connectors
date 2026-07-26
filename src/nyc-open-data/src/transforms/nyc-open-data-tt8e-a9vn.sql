-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "providertype",
    "dfta_id",
    "contractyear",
    "sponsorname",
    "programname",
    "servicefromdate",
    strptime("servicetodate", '%m/%d/%Y')::DATE AS servicetodate,
    "entrytype",
    "reportedamount"
FROM "nyc-open-data-tt8e-a9vn"
