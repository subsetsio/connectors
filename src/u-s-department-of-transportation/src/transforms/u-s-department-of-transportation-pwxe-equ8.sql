-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("requestid" AS BIGINT) AS requestid,
    "status",
    CAST("driverid" AS BIGINT) AS driverid,
    CAST("vehicleid" AS BIGINT) AS vehicleid,
    CAST("wheelchairs" AS BIGINT) AS wheelchairs,
    "rideshared",
    CAST("sharedduration" AS DOUBLE) AS sharedduration,
    CAST("passengers" AS BIGINT) AS passengers,
    "booking",
    "preference",
    "month",
    "requestedpickup",
    "requesteddropoff",
    "originalpickup",
    "cancellationahead",
    "cancellationsource",
    "noshow",
    "arrivaltime",
    "pickuptime",
    "dropofftime",
    CAST("ridedist" AS DOUBLE) AS ridedist,
    CAST("rideduration" AS DOUBLE) AS rideduration,
    CAST("directduration" AS DOUBLE) AS directduration,
    "lastpickup",
    "lastdropoff",
    CAST("lastduration" AS DOUBLE) AS lastduration,
    "rating",
    "pickupstart",
    "pickupend",
    "vehiclepickup",
    "vehicledropoff",
    "pickupstatus"
FROM "u-s-department-of-transportation-pwxe-equ8"
