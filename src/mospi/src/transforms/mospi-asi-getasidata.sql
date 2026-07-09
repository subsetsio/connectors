-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `state` and `nic_code` both carry all-India / all-industry aggregate members alongside the individual states and NIC classes — filter before summing.
-- caution: `year` is a fiscal-year label (e.g. '2019-20'), not a calendar year.
-- caution: `unit` varies by `indicator`; values are only comparable within one indicator.
SELECT
    CAST("nic_classification" AS BIGINT) AS nic_classification,
    "year",
    "state",
    "sector",
    "indicator",
    "nic_code",
    "nic_description",
    "nic_type",
    CAST("value" AS BIGINT) AS value,
    "unit"
FROM "mospi-asi-getasidata"
