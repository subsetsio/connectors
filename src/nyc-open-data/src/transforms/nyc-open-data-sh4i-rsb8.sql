-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "district",
    "physicalid",
    "roadwaytype",
    "segmentlength",
    "shape__length" AS shape_length,
    "snowpriority",
    "streetname",
    "line",
    "objectid"
FROM "nyc-open-data-sh4i-rsb8"
