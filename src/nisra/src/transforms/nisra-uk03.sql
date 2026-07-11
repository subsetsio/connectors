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
    CAST("HH_FAMILY_COMPOSITION_AGG15" AS BIGINT) AS hh_family_composition_agg15,
    "Household composition" AS household_composition,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-uk03"
