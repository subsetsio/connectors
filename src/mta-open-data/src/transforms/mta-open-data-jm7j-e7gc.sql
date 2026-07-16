-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "date",
    "event_description",
    "am_peak_late",
    "am_peak_canceled",
    "am_peak_terminated",
    "pm_peak_late",
    "pm_peak_canceled",
    "pm_peak_terminated",
    "off_peak_late",
    "off_peak_canceled",
    "off_peak_terminated"
FROM "mta-open-data-jm7j-e7gc"
