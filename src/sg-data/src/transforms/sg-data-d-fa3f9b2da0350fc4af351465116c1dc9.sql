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
    "MainlandChina_HongKongAndMacao_Total" AS mainlandchina_hongkongandmacao_total,
    "MainlandChina_HongKongAndMacao_Males" AS mainlandchina_hongkongandmacao_males,
    "MainlandChina_HongKongAndMacao_Females" AS mainlandchina_hongkongandmacao_females,
    "India_Pakistan_BangladeshAndSriLanka_Total" AS india_pakistan_bangladeshandsrilanka_total,
    "India_Pakistan_BangladeshAndSriLanka_Males" AS india_pakistan_bangladeshandsrilanka_males,
    "India_Pakistan_BangladeshAndSriLanka_Females" AS india_pakistan_bangladeshandsrilanka_females,
    "Indonesia_Total" AS indonesia_total,
    "Indonesia_Males" AS indonesia_males,
    "Indonesia_Females" AS indonesia_females,
    "OtherAsianCountries_Total" AS otherasiancountries_total,
    "OtherAsianCountries_Males" AS otherasiancountries_males,
    "OtherAsianCountries_Females" AS otherasiancountries_females,
    "EuropeanCountries_Total" AS europeancountries_total,
    "EuropeanCountries_Males" AS europeancountries_males,
    "EuropeanCountries_Females" AS europeancountries_females,
    "USAAndCanada_Total" AS usaandcanada_total,
    "USAAndCanada_Males" AS usaandcanada_males,
    "USAAndCanada_Females" AS usaandcanada_females,
    "AustraliaAndNewZealand_Total" AS australiaandnewzealand_total,
    "AustraliaAndNewZealand_Males" AS australiaandnewzealand_males,
    "AustraliaAndNewZealand_Females" AS australiaandnewzealand_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-fa3f9b2da0350fc4af351465116c1dc9"
