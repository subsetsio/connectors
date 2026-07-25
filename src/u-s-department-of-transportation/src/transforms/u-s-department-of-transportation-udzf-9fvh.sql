-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("data_dte" AS TIMESTAMP) AS data_dte,
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("usg_apt_id" AS BIGINT) AS usg_apt_id,
    "usg_apt",
    CAST("usg_wac" AS BIGINT) AS usg_wac,
    CAST("fg_apt_id" AS BIGINT) AS fg_apt_id,
    "fg_apt",
    CAST("fg_wac" AS BIGINT) AS fg_wac,
    CAST("airlineid" AS BIGINT) AS airlineid,
    "carrier",
    CAST("carriergroup" AS BIGINT) AS carriergroup,
    "type",
    CAST("scheduled" AS BIGINT) AS scheduled,
    CAST("charter" AS BIGINT) AS charter,
    CAST("total" AS BIGINT) AS total,
    "primary_key"
FROM "u-s-department-of-transportation-udzf-9fvh"
