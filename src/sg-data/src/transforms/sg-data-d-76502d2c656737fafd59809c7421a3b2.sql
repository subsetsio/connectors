-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Thousands" AS thousands,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Singapore_Total" AS singapore_total,
    "Singapore_Males" AS singapore_males,
    "Singapore_Females" AS singapore_females,
    "OutsideSingapore_Total_Total" AS outsidesingapore_total_total,
    "OutsideSingapore_Total_Males" AS outsidesingapore_total_males,
    "OutsideSingapore_Total_Females" AS outsidesingapore_total_females,
    "OutsideSingapore_UK_Total" AS outsidesingapore_uk_total,
    "OutsideSingapore_UK_Males" AS outsidesingapore_uk_males,
    "OutsideSingapore_UK_Females" AS outsidesingapore_uk_females,
    "OutsideSingapore_USAandCanada_Total" AS outsidesingapore_usaandcanada_total,
    "OutsideSingapore_USAandCanada_Males" AS outsidesingapore_usaandcanada_males,
    "OutsideSingapore_USAandCanada_Females" AS outsidesingapore_usaandcanada_females,
    "OutsideSingapore_AustraliaAndNewZealand_Total" AS outsidesingapore_australiaandnewzealand_total,
    "OutsideSingapore_AustraliaAndNewZealand_Males" AS outsidesingapore_australiaandnewzealand_males,
    "OutsideSingapore_AustraliaAndNewZealand_Females" AS outsidesingapore_australiaandnewzealand_females,
    "OutsideSingapore_China_HongKongAndMacao_Total" AS outsidesingapore_china_hongkongandmacao_total,
    "OutsideSingapore_China_HongKongAndMacao_Males" AS outsidesingapore_china_hongkongandmacao_males,
    "OutsideSingapore_China_HongKongAndMacao_Females" AS outsidesingapore_china_hongkongandmacao_females,
    "OutsideSingapore_India_Total" AS outsidesingapore_india_total,
    "OutsideSingapore_India_Males" AS outsidesingapore_india_males,
    "OutsideSingapore_India_Females" AS outsidesingapore_india_females,
    "OutsideSingapore_Others_Total" AS outsidesingapore_others_total,
    "OutsideSingapore_Others_Males" AS outsidesingapore_others_males,
    "OutsideSingapore_Others_Females" AS outsidesingapore_others_females
FROM "sg-data-d-76502d2c656737fafd59809c7421a3b2"
