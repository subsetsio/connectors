-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The current raw snapshot is empty; consumers should treat this table as an upstream placeholder until a non-empty source update lands.
SELECT
    "event_id",
    "description",
    "start_date",
    "end_date",
    "creation_date",
    "confirmed_timestamp",
    "update_date",
    "start_latitude",
    "start_longitude",
    "end_latitude",
    "end_longitude",
    "road_name_1",
    "road_name_2",
    "beginning_cross_street",
    "end_cross_street",
    "direction",
    "weather"
FROM "u-s-department-of-transportation-ayqp-ckmi"
