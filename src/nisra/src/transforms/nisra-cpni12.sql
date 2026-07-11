-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Census year" AS census_year,
    "CountyLGD" AS countylgd,
    "County and Local Government District" AS county_and_local_government_district,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-cpni12"
