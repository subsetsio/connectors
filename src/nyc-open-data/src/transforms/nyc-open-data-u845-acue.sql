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
    "entrytype",
    "budgetlineamount"
FROM "nyc-open-data-u845-acue"
