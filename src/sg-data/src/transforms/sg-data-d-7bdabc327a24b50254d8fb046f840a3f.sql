-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Malay_Total" AS malay_total,
    "Malay_Males" AS malay_males,
    "Malay_Females" AS malay_females,
    "Javanese_Total" AS javanese_total,
    "Javanese_Males" AS javanese_males,
    "Javanese_Females" AS javanese_females,
    "Boyanese_Total" AS boyanese_total,
    "Boyanese_Males" AS boyanese_males,
    "Boyanese_Females" AS boyanese_females,
    "OtherMalays_Total" AS othermalays_total,
    "OtherMalays_Males" AS othermalays_males,
    "OtherMalays_Females" AS othermalays_females
FROM "sg-data-d-7bdabc327a24b50254d8fb046f840a3f"
