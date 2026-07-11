-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field ethnicity and race" AS field_ethnicity_and_race,
    "1979",
    "1984",
    "1989",
    "1994",
    "1999",
    "2004",
    "2009",
    "2014",
    "2019",
    "2024"
FROM "ncses-nsf25349-tab001-011"
