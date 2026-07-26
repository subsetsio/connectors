-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "base_license_number",
    "base_name",
    "dba",
    "_year" AS year,
    "_month" AS month,
    "month_name",
    "total_dispatched_trips",
    "total_dispatched_shared_trips",
    "unique_dispatched_vehicles"
FROM "nyc-open-data-2v9c-2k7f"
