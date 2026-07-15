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
    "OutsideSingapore_Total_Total" AS outsidesingapore_total_total,
    "OutsideSingapore_Total_Males" AS outsidesingapore_total_males,
    "OutsideSingapore_Total_Females" AS outsidesingapore_total_females,
    "OutsideSingapore_UnitedKingdom_Total" AS outsidesingapore_unitedkingdom_total,
    "OutsideSingapore_UnitedKingdom_Males" AS outsidesingapore_unitedkingdom_males,
    "OutsideSingapore_UnitedKingdom_Females" AS outsidesingapore_unitedkingdom_females,
    "OutsideSingapore_USA_Total" AS outsidesingapore_usa_total,
    "OutsideSingapore_USA_Males" AS outsidesingapore_usa_males,
    "OutsideSingapore_USA_Females" AS outsidesingapore_usa_females,
    "OutsideSingapore_Canada_Total" AS outsidesingapore_canada_total,
    "OutsideSingapore_Canada_Males" AS outsidesingapore_canada_males,
    "OutsideSingapore_Canada_Females" AS outsidesingapore_canada_females,
    "OutsideSingapore_AustraliaandNewZealand_Total" AS outsidesingapore_australiaandnewzealand_total,
    "OutsideSingapore_AustraliaandNewZealand_Males" AS outsidesingapore_australiaandnewzealand_males,
    "OutsideSingapore_AustraliaandNewZealand_Females" AS outsidesingapore_australiaandnewzealand_females,
    "OutsideSingapore_China_HongKongandTaiwan_Total" AS outsidesingapore_china_hongkongandtaiwan_total,
    "OutsideSingapore_China_HongKongandTaiwan_Males" AS outsidesingapore_china_hongkongandtaiwan_males,
    "OutsideSingapore_China_HongKongandTaiwan_Females" AS outsidesingapore_china_hongkongandtaiwan_females,
    "OutsideSingapore_India_Total" AS outsidesingapore_india_total,
    "OutsideSingapore_India_Males" AS outsidesingapore_india_males,
    "OutsideSingapore_India_Females" AS outsidesingapore_india_females,
    "OutsideSingapore_Others_Total" AS outsidesingapore_others_total,
    "OutsideSingapore_Others_Males" AS outsidesingapore_others_males,
    "OutsideSingapore_Others_Females" AS outsidesingapore_others_females
FROM "sg-data-d-f3499c10cd743047c8ba86f338b73ba6"
