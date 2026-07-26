-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group_of_cash_assistance_application_head_of_household",
    "date_from",
    strptime("date_to", '%m/%d/%Y')::DATE AS date_to,
    "ac",
    "deny",
    "wd",
    "total"
FROM "nyc-open-data-auj6-ur3j"
