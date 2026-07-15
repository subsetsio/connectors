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
    "Eurasian_Total" AS eurasian_total,
    "Eurasian_Males" AS eurasian_males,
    "Eurasian_Females" AS eurasian_females,
    "Caucasian_Total" AS caucasian_total,
    "Caucasian_Males" AS caucasian_males,
    "Caucasian_Females" AS caucasian_females,
    "Arab_Total" AS arab_total,
    "Arab_Males" AS arab_males,
    "Arab_Females" AS arab_females,
    "Filipino_Total" AS filipino_total,
    "Filipino_Males" AS filipino_males,
    "Filipino_Females" AS filipino_females,
    "Thai_Total" AS thai_total,
    "Thai_Males" AS thai_males,
    "Thai_Females" AS thai_females,
    "Japanese_Total" AS japanese_total,
    "Japanese_Males" AS japanese_males,
    "Japanese_Females" AS japanese_females,
    "Others_Total" AS others_total,
    "Others_Males" AS others_males,
    "Others_Females" AS others_females
FROM "sg-data-d-33e6da19b3163077d293d77a2aa24e02"
