-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of",
    "jurisdiction_of_occurrence",
    "urban_rural_classification",
    "year",
    "month",
    "time_period",
    "total_deaths",
    "drug_overdose_deaths"
FROM "nchs-dtm2-meqi"
