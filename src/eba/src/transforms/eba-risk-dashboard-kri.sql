-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The period is an integer YYYYMM reference-period code, not a calendar date.
-- caution: Rows mix country values with EU/EEA aggregate geographies; filter `country` before summing or comparing peer groups.
SELECT
    "period",
    "country",
    "indicator_code",
    "indicator_name",
    "value"
FROM "eba-risk-dashboard-kri"
