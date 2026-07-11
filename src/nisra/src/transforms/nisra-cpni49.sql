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
    "MeansOfTravel" AS meansoftravel,
    "Means of travel" AS means_of_travel,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-cpni49"
