-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains state rows and United States aggregate rows in the same table; filter State Type before summing across states.
-- caution: Metric type, fuel or technology, and unit are encoded as row values rather than separate tables, so filter Category, Variable, Subcategory, and Unit before comparing or aggregating Value.
SELECT
    "Country" AS country,
    "Country code" AS country_code,
    "State" AS state,
    "State code" AS state_code,
    "State type" AS state_type,
    "Year" AS year,
    "Category" AS category,
    "Subcategory" AS subcategory,
    "Variable" AS variable,
    "Unit" AS unit,
    "Value" AS value,
    "YoY absolute change" AS yoy_absolute_change,
    "YoY % change" AS yoy_change
FROM "ember-us-yearly"
