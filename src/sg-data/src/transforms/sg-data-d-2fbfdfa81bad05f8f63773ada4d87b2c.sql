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
    "NoReligion_Total" AS noreligion_total,
    "NoReligion_Males" AS noreligion_males,
    "NoReligion_Females" AS noreligion_females,
    "Buddhism_Total" AS buddhism_total,
    "Buddhism_Males" AS buddhism_males,
    "Buddhism_Females" AS buddhism_females,
    "Taoism_Total" AS taoism_total,
    "Taoism_Males" AS taoism_males,
    "Taoism_Females" AS taoism_females,
    "Islam_Total" AS islam_total,
    "Islam_Males" AS islam_males,
    "Islam_Females" AS islam_females,
    "Hinduism_Total" AS hinduism_total,
    "Hinduism_Males" AS hinduism_males,
    "Hinduism_Females" AS hinduism_females,
    "Sikhism_Total" AS sikhism_total,
    "Sikhism_Males" AS sikhism_males,
    "Sikhism_Females" AS sikhism_females,
    "Christianity_Catholic_Total" AS christianity_catholic_total,
    "Christianity_Catholic_Males" AS christianity_catholic_males,
    "Christianity_Catholic_Females" AS christianity_catholic_females,
    "Christianity_OtherChristians_Total" AS christianity_otherchristians_total,
    "Christianity_OtherChristians_Males" AS christianity_otherchristians_males,
    "Christianity_OtherChristians_Females" AS christianity_otherchristians_females,
    "OtherReligions_Total" AS otherreligions_total,
    "OtherReligions_Males" AS otherreligions_males,
    "OtherReligions_Females" AS otherreligions_females
FROM "sg-data-d-2fbfdfa81bad05f8f63773ada4d87b2c"
