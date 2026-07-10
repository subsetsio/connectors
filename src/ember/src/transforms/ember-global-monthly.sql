-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains countries, regions, and global or multi-country aggregate rows in the same table; filter geography fields before summing across areas.
-- caution: Metric type, fuel or technology, and unit are encoded as row values rather than separate tables, so filter Category, Variable, Subcategory, and Unit before comparing or aggregating Value.
SELECT
    "Area" AS area,
    "ISO 3 code" AS iso_3_code,
    "Date" AS date,
    "Area type" AS area_type,
    "Continent" AS continent,
    "Ember region" AS ember_region,
    "EU" AS eu,
    "OECD" AS oecd,
    "G20" AS g20,
    "G7" AS g7,
    "ASEAN" AS asean,
    "Category" AS category,
    "Subcategory" AS subcategory,
    "Variable" AS variable,
    "Unit" AS unit,
    "Value" AS value,
    "YoY absolute change" AS yoy_absolute_change,
    "YoY % change" AS yoy_change
FROM "ember-global-monthly"
