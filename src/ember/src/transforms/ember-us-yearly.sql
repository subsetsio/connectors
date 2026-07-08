SELECT
CAST("Year" AS INTEGER) AS year,
"Country"                       AS country,
"Country code"                  AS country_code,
"State"                         AS state,
"State code"                    AS state_code,
"State type"                    AS state_type,
"Category"                      AS category,
"Subcategory"                   AS subcategory,
"Variable"                      AS variable,
"Unit"                          AS unit,
CAST("Value" AS DOUBLE)         AS value,
CAST("YoY absolute change" AS DOUBLE) AS yoy_absolute_change,
CAST("YoY % change" AS DOUBLE)        AS yoy_percent_change
FROM "ember-us-yearly"
WHERE "Value" IS NOT NULL
