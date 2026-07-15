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
    "Singapore_Total" AS singapore_total,
    "Singapore_Males" AS singapore_males,
    "Singapore_Females" AS singapore_females,
    "Malaysia_Total" AS malaysia_total,
    "Malaysia_Males" AS malaysia_males,
    "Malaysia_Females" AS malaysia_females,
    "MainlandChina_Total" AS mainlandchina_total,
    "MainlandChina_Males" AS mainlandchina_males,
    "MainlandChina_Females" AS mainlandchina_females,
    "India_Total" AS india_total,
    "India_Males" AS india_males,
    "India_Females" AS india_females,
    "Indonesia_Total" AS indonesia_total,
    "Indonesia_Males" AS indonesia_males,
    "Indonesia_Females" AS indonesia_females,
    "OtherAsianCountries_Regions_Total" AS otherasiancountries_regions_total,
    "OtherAsianCountries_Regions_Males" AS otherasiancountries_regions_males,
    "OtherAsianCountries_Regions_Females" AS otherasiancountries_regions_females,
    "Europe_Total" AS europe_total,
    "Europe_Males" AS europe_males,
    "Europe_Females" AS europe_females,
    "USAandCanada_Total" AS usaandcanada_total,
    "USAandCanada_Males" AS usaandcanada_males,
    "USAandCanada_Females" AS usaandcanada_females,
    "AustraliaandNewZealand_Total" AS australiaandnewzealand_total,
    "AustraliaandNewZealand_Males" AS australiaandnewzealand_males,
    "AustraliaandNewZealand_Females" AS australiaandnewzealand_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-3ba797b9aab692919a223cae32029b41"
