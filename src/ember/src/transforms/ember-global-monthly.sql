SELECT
CAST("Date" AS DATE) AS date,
"Area"                          AS area,
"ISO 3 code"                    AS iso3_code,
"Area type"                     AS area_type,
"Continent"                     AS continent,
"Ember region"                  AS ember_region,
CAST("EU" AS BOOLEAN)           AS eu,
CAST("OECD" AS BOOLEAN)         AS oecd,
CAST("G20" AS BOOLEAN)          AS g20,
CAST("G7" AS BOOLEAN)           AS g7,
CAST("ASEAN" AS BOOLEAN)        AS asean,
"Category"                      AS category,
"Subcategory"                   AS subcategory,
"Variable"                      AS variable,
"Unit"                          AS unit,
CAST("Value" AS DOUBLE)         AS value,
CAST("YoY absolute change" AS DOUBLE) AS yoy_absolute_change,
CAST("YoY % change" AS DOUBLE)        AS yoy_percent_change
FROM "ember-global-monthly"
WHERE "Value" IS NOT NULL
