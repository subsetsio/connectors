-- caution: Region_City mixes aggregation levels (National totals beside City /
-- Municipality / Region / District / Ward rows) -- filter area_type before aggregating.
-- caution: (area_name, country, indicator, year, source) does NOT identify a row; the
-- source stacks differing values under identical labels. object_id is the only identity.
-- caution: `indicator` mixes component categories with their own totals
-- ("Total piped" alongside "Piped water into dwelling/ plot") -- never sum across indicators.
SELECT
    "ObjectId"::BIGINT AS object_id,
    "Continent" AS continent,
    "M49_classification" AS m49_classification,
    "Region" AS m49_region,
    "Country" AS country,
    "Region_City" AS area_type,
    "Region_City_Name" AS area_name,
    "Year"::BIGINT AS year,
    "Source" AS source,
    "Indicator" AS indicator,
    "Value"::DOUBLE AS value_percent
FROM "un-habitat-0bb9c1570c474f77a994f17d60adcf4c"
