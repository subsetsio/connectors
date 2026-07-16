-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "transit_timestamp",
    "date",
    "hour",
    "facility_id",
    "facility",
    "direction",
    "payment_method",
    "vehicle_class",
    "vehicle_class_description",
    "vehicle_class_category",
    "traffic_count"
FROM "mta-open-data-ebfx-2m7v"
