-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("report_date" AS TIMESTAMP) AS report_date,
    "manufacturer",
    "recall_campaign",
    CAST("priority_group" AS BIGINT) AS priority_group,
    "driver_passenger",
    CAST("total_air_bags_affected" AS BIGINT) AS total_air_bags_affected,
    CAST("total_inflators_repaired" AS BIGINT) AS total_inflators_repaired,
    CAST("scrapped" AS BIGINT) AS scrapped,
    CAST("exported" AS BIGINT) AS exported,
    CAST("stolen" AS BIGINT) AS stolen,
    CAST("other" AS BIGINT) AS other,
    CAST("nonresponsive" AS BIGINT) AS nonresponsive,
    CAST("affirmative_refusal" AS BIGINT) AS affirmative_refusal,
    CAST("aftermarket_modification" AS BIGINT) AS aftermarket_modification,
    CAST("vehicle_degradation" AS BIGINT) AS vehicle_degradation,
    CAST("net_inflators_affected" AS BIGINT) AS net_inflators_affected,
    CAST("net_inflators_remaining" AS BIGINT) AS net_inflators_remaining,
    CAST("completion_rate" AS DOUBLE) AS completion_rate
FROM "u-s-department-of-transportation-8u28-hw9f"
