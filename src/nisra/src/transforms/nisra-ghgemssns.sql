-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "CTRY24CD" AS ctry24cd,
    "Country" AS country,
    "TES_SUBSECTOR" AS tes_subsector,
    "TES subsector" AS tes_subsector_2,
    "POLLUTANTS" AS pollutants,
    "Pollutants Label" AS pollutants_label,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-ghgemssns"
