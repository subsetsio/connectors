-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the PSMSL metric product and is not controlled to the continuous Revised Local Reference datum; use it separately from RLR series.
-- caution: Rows are distinguished by PSMSL data and missing-data flags as well as station and month, so filter or group flags deliberately when building station-month series.
SELECT
    "station_id",
    "decimal_year",
    "year",
    "month",
    "msl_mm",
    "missing_flag",
    "data_flag"
FROM "psmsl-met-monthly"
