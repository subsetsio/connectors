-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country_Name" AS country_name,
    CAST("Year_Text" AS BIGINT) AS year_text,
    CAST("Year_Date&Time" AS BIGINT) AS year_date_time,
    "Income" AS income,
    "Region" AS region,
    "Variable_Description" AS variable_description,
    "Variable_ID" AS variable_id,
    CAST("Value" AS DOUBLE) AS value,
    "source_resource"
FROM "idb-data-associated-with-wealth-financial-intermediation-and-saving-in-latin-am"
