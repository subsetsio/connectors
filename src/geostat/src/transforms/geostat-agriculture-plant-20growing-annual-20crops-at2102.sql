-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "region",
    "type",
    "crop_name",
    "value"
FROM "geostat-agriculture-plant-20growing-annual-20crops-at2102"
