-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census year" AS BIGINT) AS census_year,
    "CTRY24CD" AS ctry24cd,
    "Country" AS country,
    CAST("ACCOMMODATION_TYPE" AS BIGINT) AS accommodation_type,
    "Accommodation type" AS accommodation_type_2,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-uk11"
