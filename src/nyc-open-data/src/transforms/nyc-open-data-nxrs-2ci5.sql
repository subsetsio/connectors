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
    "serviceid",
    "servicename",
    "budgetedunits"
FROM "nyc-open-data-nxrs-2ci5"
