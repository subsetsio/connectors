-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census year" AS BIGINT) AS census_year,
    "DEA2014" AS dea2014,
    "District Electoral Area" AS district_electoral_area,
    "AGE_BAND_AGG17" AS age_band_agg17,
    "Age (17 cats)" AS age_17_cats,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-ks102nidea"
