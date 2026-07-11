-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "AA2024" AS aa2024,
    "Assembly Area (2024)" AS assembly_area_2024,
    "broadage11",
    "Broad age band (11 cat)" AS broad_age_band_11_cat,
    "Sex" AS sex,
    "Sex Label" AS sex_label,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-mye01t014"
