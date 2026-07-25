-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    CAST("vehicles_weighed_fixed" AS BIGINT) AS vehicles_weighed_fixed,
    CAST("vehicles_weighed_wim" AS BIGINT) AS vehicles_weighed_wim,
    CAST("vehicles_weighed_portable" AS BIGINT) AS vehicles_weighed_portable,
    CAST("vehicles_weighed_semi_portable" AS BIGINT) AS vehicles_weighed_semi_portable,
    CAST("oversize_violation_current_year" AS BIGINT) AS oversize_violation_current_year,
    CAST("overweight_violation_current_year" AS BIGINT) AS overweight_violation_current_year,
    CAST("non_divisible_trip_permits" AS BIGINT) AS non_divisible_trip_permits,
    CAST("non_divisible_annual_permits" AS BIGINT) AS non_divisible_annual_permits,
    CAST("divisible_trip_permits" AS BIGINT) AS divisible_trip_permits,
    CAST("divisible_annual_permits" AS BIGINT) AS divisible_annual_permits
FROM "u-s-department-of-transportation-mt5m-skz3"
