-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field and time to degree - All fields" AS field_and_time_to_degree_all_fields,
    "1974 - All fields" AS "1974_all_fields",
    "1979 - All fields" AS "1979_all_fields",
    "1984 - All fields" AS "1984_all_fields",
    "1989 - All fields" AS "1989_all_fields",
    "1994 - All fields" AS "1994_all_fields",
    "1999 - All fields" AS "1999_all_fields",
    "2004 - All fields" AS "2004_all_fields",
    "2009 - All fields" AS "2009_all_fields",
    "2014 - All fields" AS "2014_all_fields",
    "2019 - All fields" AS "2019_all_fields",
    "2024 - All fields" AS "2024_all_fields"
FROM "ncses-nsf25349-tab001-012"
