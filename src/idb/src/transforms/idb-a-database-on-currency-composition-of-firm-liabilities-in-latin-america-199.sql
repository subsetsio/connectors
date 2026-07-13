-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country" AS country,
    "Table_name" AS table_name,
    "Asset_Category" AS asset_category,
    "Asset_Composition" AS asset_composition,
    CAST("Year" AS BIGINT) AS year,
    CAST("Year_Date" AS BIGINT) AS year_date,
    "Methodology" AS methodology,
    CAST("Value" AS BIGINT) AS value,
    "Notes" AS notes,
    "source_resource"
FROM "idb-a-database-on-currency-composition-of-firm-liabilities-in-latin-america-199"
