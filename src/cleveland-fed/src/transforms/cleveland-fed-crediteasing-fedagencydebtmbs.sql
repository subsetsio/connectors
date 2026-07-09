-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weekly (Wednesday) balance levels in millions of US dollars, not flows.
-- caution: `federal_agency_debt_and_mortgage_backed_securities_purchases` is the total of the two component columns beside it — summing all three columns double-counts.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "mortgage_backed_securities",
    "federal_agency_debt_securities",
    "federal_agency_debt_and_mortgage_backed_securities_purchases"
FROM "cleveland-fed-crediteasing-fedagencydebtmbs"
