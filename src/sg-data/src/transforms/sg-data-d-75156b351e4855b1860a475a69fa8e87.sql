-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Singapore_Total" AS singapore_total,
    "Singapore_Males" AS singapore_males,
    "Singapore_Females" AS singapore_females,
    "OutsideSingapore_Total" AS outsidesingapore_total,
    "OutsideSingapore_Males" AS outsidesingapore_males,
    "OutsideSingapore_Females" AS outsidesingapore_females
FROM "sg-data-d-75156b351e4855b1860a475a69fa8e87"
