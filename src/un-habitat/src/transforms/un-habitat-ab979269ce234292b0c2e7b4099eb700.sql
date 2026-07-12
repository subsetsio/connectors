-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains urban-share projection values for multiple countries or areas across years; filter the geography fields before aggregating.
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
