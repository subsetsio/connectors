-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide table: one column per five-year period from Y2000 to Y2050, so the observation period is a column name rather than a value.
-- caution: Values from 2025 onward are projections, not observations - the underlying source is the UN World Urbanization Prospects 2018 revision.
-- caution: The area column mixes M49 regional aggregates with individual countries. Filter before averaging or regions are weighted alongside their own members.
-- caution: The last rows of the table are the source's own spreadsheet footer (a Metadata marker, the table title and a citation) carrying no area and no values.
-- caution: Values are a percentage of each area's total population, so they cannot be summed across areas.
SELECT
    "source_item_id",
    "source_title",
    "source_type",
    "source_kind",
    "source_name",
    "source_row_number",
    "Region__subregion__country_or_a" AS region_subregion_country_or_a,
    "Data_Units" AS data_units,
    "Y2000" AS y2000,
    "Y2005" AS y2005,
    "Y2010" AS y2010,
    "Y2015" AS y2015,
    "Y2020" AS y2020,
    "Y2025" AS y2025,
    "Y2030" AS y2030,
    "Y2035" AS y2035,
    "Y2040" AS y2040,
    "Y2045" AS y2045,
    "Y2050" AS y2050,
    "ObjectId" AS objectid
FROM "un-habitat-ab979269ce234292b0c2e7b4099eb700"
