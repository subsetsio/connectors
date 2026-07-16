-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "violation_id",
    "vehicle_id",
    "first_occurrence",
    "last_occurrence",
    "violation_status",
    "violation_type",
    "bus_route_id",
    "violation_latitude",
    "violation_longitude",
    "stop_id",
    "stop_name",
    "bus_stop_latitude",
    "bus_stop_longitude",
    "violation_georeference",
    "bus_stop_georeference"
FROM "mta-open-data-kh8p-hcbm"
