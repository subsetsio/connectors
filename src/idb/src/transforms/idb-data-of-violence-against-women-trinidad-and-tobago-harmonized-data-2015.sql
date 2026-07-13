-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country" AS country,
    "Category" AS category,
    "Indicator" AS indicator,
    "Sub-indicator" AS sub_indicator,
    "Answer" AS answer,
    CAST("Value" AS BIGINT) AS value,
    CAST("Percentage" AS DOUBLE) AS percentage,
    "Notes" AS notes,
    "source_resource"
FROM "idb-data-of-violence-against-women-trinidad-and-tobago-harmonized-data-2015"
