-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "agency",
    "fleet_name",
    "fleet_roster",
    "target_daily_in_service",
    "target_in_service",
    "actual_count_in_service",
    "average_over_fy_18_to_date",
    "seasonal_flag",
    "agency_total",
    "critical_fleet_only",
    "description"
FROM "nyc-open-data-5rzx-3686"
