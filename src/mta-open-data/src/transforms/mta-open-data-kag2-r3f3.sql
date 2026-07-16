-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "code",
    "name",
    "physical_asset",
    "app",
    "app_name",
    "locale",
    "language",
    "date_ny",
    "bus_box_id",
    "bus_stop_name",
    "bus_stop_type",
    "subway_id",
    "station_name",
    "train_car_type"
FROM "mta-open-data-kag2-r3f3"
