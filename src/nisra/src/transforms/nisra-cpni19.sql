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
    "AGE_BAND_AGG11" AS age_band_agg11,
    "Age (11 cats)" AS age_11_cats,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-cpni19"
