-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Personnel functions" AS personnel_functions,
    "2020 - Headcount" AS 2020_headcount,
    "2020 - FTEs" AS 2020_ftes,
    "2021 - Headcount" AS 2021_headcount,
    "2021 - FTEs" AS 2021_ftes,
    "2022 - Headcount" AS 2022_headcount,
    "2022 - FTEs" AS 2022_ftes,
    "2023 - Headcount" AS 2023_headcount,
    "2023 - FTEs" AS 2023_ftes,
    "2024 - Headcount" AS 2024_headcount,
    "2024 - FTEs" AS 2024_ftes
FROM "ncses-nsf26304-tab026"
