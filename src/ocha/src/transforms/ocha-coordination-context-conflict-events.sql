-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are aggregated conflict-event counts by event_type, location, administrative level, and period; filter those dimensions before summing events or fatalities.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    "resource_hdx_id",
    "event_type",
    "events",
    "fatalities",
    "reference_period_start",
    "reference_period_end"
FROM "ocha-coordination-context-conflict-events"
