-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The geographic area taxonomy includes countries, territories, regions and aggregate areas; filter the desired area level before summing observations joined from values.
SELECT
    CAST("geo_area_code" AS BIGINT) AS geo_area_code,
    "geo_area_name"
FROM "united-nations-geoareas"
