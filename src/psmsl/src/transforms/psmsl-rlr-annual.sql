-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are distinguished by PSMSL data and missing-data flags as well as station and year, so filter or group flags deliberately when building station-year series.
SELECT
    "station_id",
    "year",
    "msl_mm",
    "missing_flag",
    "data_flag"
FROM "psmsl-rlr-annual"
