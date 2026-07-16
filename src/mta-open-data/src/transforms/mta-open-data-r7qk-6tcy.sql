-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "division",
    "line",
    "period",
    "num_passengers",
    "additional_platform_time",
    "additional_train_time",
    "total_apt",
    "total_att",
    "over_five_mins",
    "over_five_mins_perc",
    "customer_journey_time"
FROM "mta-open-data-r7qk-6tcy"
