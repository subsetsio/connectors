-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "cv",
    CAST("ci" AS DOUBLE) AS ci,
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "uk_only",
    "geography",
    "age_groups",
    "agegroups",
    "sex",
    "sex_1",
    "sexual_orientation",
    "sexualorientation",
    "unit_of_measure",
    "unitofmeasure"
FROM "ons-sexual-orientation-by-age-and-sex"
