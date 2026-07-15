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
    "Indonesia_Total" AS indonesia_total,
    "Indonesia_Males" AS indonesia_males,
    "Indonesia_Females" AS indonesia_females,
    "MainlandChina_HongKongAndTaiwan_Total" AS mainlandchina_hongkongandtaiwan_total,
    "MainlandChina_HongKongAndTaiwan_Males" AS mainlandchina_hongkongandtaiwan_males,
    "MainlandChina_HongKongAndTaiwan_Females" AS mainlandchina_hongkongandtaiwan_females,
    "SouthAsia_Total" AS southasia_total,
    "SouthAsia_Males" AS southasia_males,
    "SouthAsia_Females" AS southasia_females,
    "OtherAsianCountries_Total" AS otherasiancountries_total,
    "OtherAsianCountries_Males" AS otherasiancountries_males,
    "OtherAsianCountries_Females" AS otherasiancountries_females,
    "EuropeanCountries_Total" AS europeancountries_total,
    "EuropeanCountries_Males" AS europeancountries_males,
    "EuropeanCountries_Females" AS europeancountries_females,
    "USAAndCanada_Total" AS usaandcanada_total,
    "USAAndCanada_Males" AS usaandcanada_males,
    "USAAndCanada_Females" AS usaandcanada_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-bce3caddda187d1162467c0cfa650673"
