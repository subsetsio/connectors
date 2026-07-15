-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DataSeries" AS dataseries,
    "2020",
    "2019",
    "2018"
FROM "sg-data-d-f40fdf4a43c62909805d3a50d8c8c1a7"
