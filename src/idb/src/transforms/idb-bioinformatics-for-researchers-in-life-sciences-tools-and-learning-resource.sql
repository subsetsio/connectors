-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Tool_Name" AS tool_name,
    CAST("ID" AS BIGINT) AS id,
    "Main_URL" AS main_url,
    "Usage" AS usage,
    "Biotech_Fields" AS biotech_fields,
    "Description" AS description,
    "Technology_Type" AS technology_type,
    "Level_of_Complexity" AS level_of_complexity,
    "Pricing_Model" AS pricing_model,
    "Pricing_Detail" AS pricing_detail,
    "Documentation_and_Tutorials" AS documentation_and_tutorials,
    "Alternative_URLs" AS alternative_urls,
    "Learning__Resources" AS learning_resources,
    "Notes" AS notes,
    CAST("Year_Published" AS BIGINT) AS year_published,
    "Country_or_Region" AS country_or_region,
    "source_resource"
FROM "idb-bioinformatics-for-researchers-in-life-sciences-tools-and-learning-resource"
