-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "county_name",
    CAST("population_density_1900" AS DOUBLE) AS population_density_1900,
    CAST("population_density_1910" AS DOUBLE) AS population_density_1910,
    CAST("population_density_1920" AS DOUBLE) AS population_density_1920,
    CAST("population_density_1930" AS DOUBLE) AS population_density_1930,
    CAST("population_density_1940" AS DOUBLE) AS population_density_1940,
    CAST("population_density_1950" AS DOUBLE) AS population_density_1950,
    CAST("population_density_1960" AS DOUBLE) AS population_density_1960,
    CAST("population_density_1970" AS DOUBLE) AS population_density_1970,
    CAST("population_density_1980" AS DOUBLE) AS population_density_1980,
    CAST("population_density_1990" AS DOUBLE) AS population_density_1990,
    CAST("population_density_2000" AS DOUBLE) AS population_density_2000,
    CAST("population_density_2010" AS DOUBLE) AS population_density_2010,
    CAST("population_density_2020" AS DOUBLE) AS population_density_2020
FROM "washington-ofm-socrata-e6ip-wkqq"
