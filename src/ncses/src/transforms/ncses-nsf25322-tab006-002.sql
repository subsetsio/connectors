-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Sex ethnicity race and occupation" AS sex_ethnicity_race_and_occupation,
    "2003",
    "2010",
    "2013",
    "2015",
    "2017",
    "2019",
    "2021",
    "2023a"
FROM "ncses-nsf25322-tab006-002"
