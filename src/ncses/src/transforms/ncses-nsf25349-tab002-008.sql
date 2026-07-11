-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Region and country or economy of citizenship" AS region_and_country_or_economy_of_citizenship,
    "2018–24 - Number" AS "2018_24_number",
    "2018–24 - % staying" AS "2018_24_staying",
    "2018 - Number" AS "2018_number",
    "2018 - % staying" AS "2018_staying",
    "2019 - Number" AS "2019_number",
    "2019 - % staying" AS "2019_staying",
    "2020 - Number" AS "2020_number",
    "2020 - % staying" AS "2020_staying",
    "2021 - Number" AS "2021_number",
    "2021 - % staying" AS "2021_staying",
    "2022 - Number" AS "2022_number",
    "2022 - % staying" AS "2022_staying",
    "2023 - Number" AS "2023_number",
    "2023 - % staying" AS "2023_staying",
    "2024 - Number" AS "2024_number",
    "2024 - % staying" AS "2024_staying"
FROM "ncses-nsf25349-tab002-008"
