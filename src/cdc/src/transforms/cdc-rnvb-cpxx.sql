-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "LocationAbbrev" AS locationabbrev,
    "LocationDesc" AS locationdesc,
    CAST("Population" AS BIGINT) AS population,
    "Topic" AS topic,
    "Measure" AS measure,
    "Submeasure" AS submeasure,
    "Data Value Unit" AS data_value_unit,
    CAST("Domestic" AS BIGINT) AS domestic,
    CAST("Imports" AS BIGINT) AS imports,
    CAST("Total" AS BIGINT) AS total,
    CAST("Domestic Per Capita" AS BIGINT) AS domestic_per_capita,
    CAST("Imports Per Capita" AS DOUBLE) AS imports_per_capita,
    CAST("Total Per Capita" AS BIGINT) AS total_per_capita
FROM "cdc-rnvb-cpxx"
