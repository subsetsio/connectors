-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census year" AS BIGINT) AS census_year,
    "COCITY" AS cocity,
    "County and City" AS county_and_city,
    "AGE" AS age,
    "Age Label" AS age_label,
    "SEX" AS sex,
    "Sex Label" AS sex_label,
    "OCCUPATIONS" AS occupations,
    "Occupations Label" AS occupations_label,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-hca18"
