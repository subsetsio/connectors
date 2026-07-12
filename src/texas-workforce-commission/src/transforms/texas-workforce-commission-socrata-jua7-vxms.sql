-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("state_id" AS BIGINT) AS state_id,
    CAST("zipcode" AS BIGINT) AS zipcode,
    CAST("reportingdate" AS TIMESTAMP) AS reportingdate,
    CAST("typecc" AS BIGINT) AS typecc,
    CAST("participation" AS BIGINT) AS participation,
    "rating",
    CAST("accrdstatus" AS BIGINT) AS accrdstatus,
    CAST("prekstandard" AS BIGINT) AS prekstandard,
    CAST("qualitymeasure" AS BIGINT) AS qualitymeasure,
    CAST("headstart" AS BIGINT) AS headstart,
    CAST("monthlyamtpaid" AS BIGINT) AS monthlyamtpaid
FROM "texas-workforce-commission-socrata-jua7-vxms"
