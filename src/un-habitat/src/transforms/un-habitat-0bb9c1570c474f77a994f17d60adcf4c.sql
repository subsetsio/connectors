-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table mixes city, country, and regional naming columns; filter the geography fields before aggregating values across places.
-- caution: Rows contain multiple indicators in percent units; filter `Indicator` before comparing or summing observations.
SELECT
    "source_item_id",
    "source_title",
    "source_type",
    "source_kind",
    "source_name",
    "source_row_number",
    "Continent" AS continent,
    "M49_classification" AS m49_classification,
    "Region" AS region,
    "Country" AS country,
    "Region_City" AS region_city,
    "Region_City_Name" AS region_city_name,
    "Year" AS year,
    "Source" AS source,
    "Indicator" AS indicator,
    "Value" AS value,
    "ObjectId" AS objectid
FROM "un-habitat-0bb9c1570c474f77a994f17d60adcf4c"
