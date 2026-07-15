-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "NoQualification_Total" AS noqualification_total,
    "NoQualification_Males" AS noqualification_males,
    "NoQualification_Females" AS noqualification_females,
    "Primary_Total" AS primary_total,
    "Primary_Males" AS primary_males,
    "Primary_Females" AS primary_females,
    "LowerSecondary_Total" AS lowersecondary_total,
    "LowerSecondary_Males" AS lowersecondary_males,
    "LowerSecondary_Females" AS lowersecondary_females,
    "Secondary_Total" AS secondary_total,
    "Secondary_Males" AS secondary_males,
    "Secondary_Females" AS secondary_females,
    "UpperSecondary_Total" AS uppersecondary_total,
    "UpperSecondary_Males" AS uppersecondary_males,
    "UpperSecondary_Females" AS uppersecondary_females
FROM "sg-data-d-5cff49f6bb923419917c1231026621bf"
