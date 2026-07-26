-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hh_id",
    "vehicle_id",
    "vehicle_num",
    "_year" AS year,
    "fuel_type",
    "hh_weight_zonal",
    "hh_weight_citywide"
FROM "nyc-open-data-qhkz-4dqm"
