-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Census year" AS census_year,
    "NIROI" AS niroi,
    "Ireland and Northern Ireland" AS ireland_and_northern_ireland,
    "LevelOfEducation" AS levelofeducation,
    "Level of education" AS level_of_education,
    "AGE_BAND_AGG4" AS age_band_agg4,
    "Age (4 cats)" AS age_4_cats,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-cpni50"
