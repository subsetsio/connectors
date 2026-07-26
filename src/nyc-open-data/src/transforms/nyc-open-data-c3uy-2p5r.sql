-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unique_id",
    "indicator_id",
    "_name" AS name,
    "measure",
    "measure_info",
    "geo_type_name",
    "geo_join_id",
    "geo_place_name",
    "time_period",
    "start_date",
    "data_value",
    "message"
FROM "nyc-open-data-c3uy-2p5r"
