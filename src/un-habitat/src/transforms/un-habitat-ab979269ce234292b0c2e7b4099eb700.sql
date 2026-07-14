-- Reshaped from the source's wide layout: one column per five-year period
-- (Y2000..Y2050) becomes one row per (area, year). Mirrors the companion table
-- un-habitat-a0ed106eb49b41e9a1989f1fe89fcb4a, which publishes the urban
-- population counts these percentages accompany.
-- The WHERE drops the source's own spreadsheet footer (a Metadata marker, the
-- table title and a citation), which carries no area and no values.
-- Data_Units is dropped: the source's own title states the unit, which is
-- folded into the value column's name and description instead.
-- caution: values from 2025 on are projections (UN World Urbanization Prospects 2018).
-- caution: `area` mixes M49 regional aggregates (e.g. "Western Asia") with countries.
SELECT
    area,
    CAST(substr(period, 2, 4) AS BIGINT) AS year,
    CAST(urban_share AS DOUBLE) AS urban_population_percent
FROM (
    SELECT
        "Region__subregion__country_or_a" AS area,
        "Y2000", "Y2005", "Y2010", "Y2015", "Y2020", "Y2025",
        "Y2030", "Y2035", "Y2040", "Y2045", "Y2050"
    FROM "un-habitat-ab979269ce234292b0c2e7b4099eb700"
    WHERE "Region__subregion__country_or_a" IS NOT NULL
)
UNPIVOT (
    urban_share FOR period IN (
        "Y2000", "Y2005", "Y2010", "Y2015", "Y2020", "Y2025",
        "Y2030", "Y2035", "Y2040", "Y2045", "Y2050"
    )
)
