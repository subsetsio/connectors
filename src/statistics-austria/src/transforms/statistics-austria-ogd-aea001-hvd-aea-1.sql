-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "economic_branch",
    "so2_in_tons",
    "nox_in_tons",
    "nmvoc_in_tons",
    "ch4_in_tons",
    "co_in_tons",
    "co2_overall_in_1_000_tons",
    "co2_from_fossil_resources_in_1_000_tons",
    "co2_from_biogeneous_resources_in_1_000_tons",
    "co2_from_other_sources_in_1_000_tons",
    "n2o_in_tons",
    "nh3_in_tons",
    "pm10_in_tons",
    "pm2_5_in_tons"
FROM "statistics-austria-ogd-aea001-hvd-aea-1"
