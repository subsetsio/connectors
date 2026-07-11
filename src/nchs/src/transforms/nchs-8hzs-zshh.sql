-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of",
    "death_year",
    "death_month",
    "jurisdiction_occurrence",
    "drug_involved",
    "time_period",
    strptime("month_ending_date", '%m/%d/%Y')::DATE AS month_ending_date,
    "drug_overdose_deaths",
    "footnote"
FROM "nchs-8hzs-zshh"
