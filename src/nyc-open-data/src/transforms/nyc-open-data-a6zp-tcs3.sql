-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "pmmr_goal",
    "critical",
    "performance_indicator",
    "actual_fy14",
    "actual_fy15",
    "actual_fy16",
    "target_fy17",
    "target_fy18",
    "_4month_actual_fy16" AS 4month_actual_fy16,
    "_4month_actual_fy17" AS 4month_actual_fy17
FROM "nyc-open-data-a6zp-tcs3"
