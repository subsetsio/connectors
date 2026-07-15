-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Hokkien_Total" AS hokkien_total,
    "Hokkien_Males" AS hokkien_males,
    "Hokkien_Females" AS hokkien_females,
    "Teochew_Total" AS teochew_total,
    "Teochew_Males" AS teochew_males,
    "Teochew_Females" AS teochew_females,
    "Cantonese_Total" AS cantonese_total,
    "Cantonese_Males" AS cantonese_males,
    "Cantonese_Females" AS cantonese_females,
    "Hakka_Total" AS hakka_total,
    "Hakka_Males" AS hakka_males,
    "Hakka_Females" AS hakka_females,
    "Hainanese_Total" AS hainanese_total,
    "Hainanese_Males" AS hainanese_males,
    "Hainanese_Females" AS hainanese_females,
    "Foochow_Total" AS foochow_total,
    "Foochow_Males" AS foochow_males,
    "Foochow_Females" AS foochow_females,
    "Henghua_Total" AS henghua_total,
    "Henghua_Males" AS henghua_males,
    "Henghua_Females" AS henghua_females,
    "Shanghainese_Total" AS shanghainese_total,
    "Shanghainese_Males" AS shanghainese_males,
    "Shanghainese_Females" AS shanghainese_females,
    "Hockchia_Total" AS hockchia_total,
    "Hockchia_Males" AS hockchia_males,
    "Hockchia_Females" AS hockchia_females,
    "OtherChinese_Total" AS otherchinese_total,
    "OtherChinese_Males" AS otherchinese_males,
    "OtherChinese_Females" AS otherchinese_females
FROM "sg-data-d-ed9c7fb9b932b02f24bf0253a84cabe4"
