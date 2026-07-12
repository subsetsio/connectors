-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are yearly exceedance summaries with monthly count columns; summing across months and value_of_year together double-counts the same exceedance information.
SELECT
    "component_id",
    "year",
    "station_id",
    "day_first",
    "day_recent",
    "value_of_year",
    "month_01",
    "month_02",
    "month_03",
    "month_04",
    "month_05",
    "month_06",
    "month_07",
    "month_08",
    "month_09",
    "month_10",
    "month_11",
    "month_12"
FROM "umweltbundesamt-transgressions"
