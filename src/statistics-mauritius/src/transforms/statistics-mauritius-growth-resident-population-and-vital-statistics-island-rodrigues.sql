-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Population_Start_of_Year" AS BIGINT) AS population_start_of_year,
    CAST("Live_Birth_Per_Year" AS BIGINT) AS live_birth_per_year,
    CAST("Death_Per_Year" AS BIGINT) AS death_per_year,
    CAST("Natural_ Increase" AS BIGINT) AS natural_increase,
    CAST("Total_Increase" AS BIGINT) AS total_increase,
    CAST("Population_End_of_Year" AS BIGINT) AS population_end_of_year,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-growth-resident-population-and-vital-statistics-island-rodrigues"
