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
    "OutsideSingapore_Australia_Total" AS outsidesingapore_australia_total,
    "OutsideSingapore_Australia_Males" AS outsidesingapore_australia_males,
    "OutsideSingapore_Australia_Females" AS outsidesingapore_australia_females,
    "OutsideSingapore_UK_Total" AS outsidesingapore_uk_total,
    "OutsideSingapore_UK_Males" AS outsidesingapore_uk_males,
    "OutsideSingapore_UK_Females" AS outsidesingapore_uk_females,
    "OutsideSingapore_Malaysia_Total" AS outsidesingapore_malaysia_total,
    "OutsideSingapore_Malaysia_Males" AS outsidesingapore_malaysia_males,
    "OutsideSingapore_Malaysia_Females" AS outsidesingapore_malaysia_females,
    "OutsideSingapore_India_Total" AS outsidesingapore_india_total,
    "OutsideSingapore_India_Males" AS outsidesingapore_india_males,
    "OutsideSingapore_India_Females" AS outsidesingapore_india_females,
    "OutsideSingapore_US_Total" AS outsidesingapore_us_total,
    "OutsideSingapore_US_Males" AS outsidesingapore_us_males,
    "OutsideSingapore_US_Females" AS outsidesingapore_us_females,
    "OutsideSingapore_MainlandChina_Total" AS outsidesingapore_mainlandchina_total,
    "OutsideSingapore_MainlandChina_Males" AS outsidesingapore_mainlandchina_males,
    "OutsideSingapore_MainlandChina_Females" AS outsidesingapore_mainlandchina_females,
    "OutsideSingapore_Others_Total" AS outsidesingapore_others_total,
    "OutsideSingapore_Others_Males" AS outsidesingapore_others_males,
    "OutsideSingapore_Others_Females" AS outsidesingapore_others_females
FROM "sg-data-d-338d4546b871143b33e64d7572a6ca26"
