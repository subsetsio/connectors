-- Reshaped from the source's wide layout: one column per five-year period
-- (Y2000..Y2050) becomes one row per (area, year).
-- The WHERE drops the source's own spreadsheet footer (a Metadata marker, the
-- table title and a citation), which carries no area and no values.
-- Data_Units is constant 'Thousand' across every real row and is folded into
-- the value column's name and description instead of being published.
-- caution: values from 2025 on are projections (UN World Urbanization Prospects 2018).
-- caution: `area` mixes M49 regional aggregates (e.g. "Western Asia") with countries.
SELECT
    area,
    CAST(substr(period, 2, 4) AS BIGINT) AS year,
    CAST(urban_population AS BIGINT) AS urban_population_thousands
FROM (
    SELECT
        "Region_subregion_country_or_are" AS area,
        "Y2000", "Y2005", "Y2010", "Y2015", "Y2020", "Y2025",
        "Y2030", "Y2035", "Y2040", "Y2045", "Y2050"
    FROM "un-habitat-a0ed106eb49b41e9a1989f1fe89fcb4a"
    WHERE "Region_subregion_country_or_are" IS NOT NULL
)
UNPIVOT (
    urban_population FOR period IN (
        "Y2000", "Y2005", "Y2010", "Y2015", "Y2020", "Y2025",
        "Y2030", "Y2035", "Y2040", "Y2045", "Y2050"
    )
)
