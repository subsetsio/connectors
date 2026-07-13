-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country" AS country,
    "Indicator" AS indicator,
    CAST("Year_Date" AS BIGINT) AS year_date,
    CAST("Year" AS BIGINT) AS year,
    CAST("Value" AS DOUBLE) AS value,
    "source_resource"
FROM "idb-structural-fiscal-balances-database-for-lac-a-tool-to-assess-fiscal-perform"
